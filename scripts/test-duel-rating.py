"""Exercise the lobby migration in a disposable, network-isolated Postgres17."""
import concurrent.futures
import json
import pathlib
import subprocess
import time
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTAINER = "cfr-rating-test-" + uuid.uuid4().hex[:10]
ROOM = "00000000-0000-0000-0000-000000000001"
A = "00000000-0000-0000-0000-000000000002"
B = "00000000-0000-0000-0000-000000000003"
OUTSIDER = "00000000-0000-0000-0000-000000000004"


def sql(query):
    return subprocess.run(
        ["docker", "exec", "-i", CONTAINER, "psql", "-h", "127.0.0.1", "-U", "postgres", "-v", "ON_ERROR_STOP=1", "-At"],
        input=query, text=True, check=True, capture_output=True,
    ).stdout.strip()


def action(kind, user=A, patch=None):
    payload = json.dumps(patch or {}).replace("'", "''")
    return f"select public.duel_lobby_action('{ROOM}', '{user}', '{kind}', '{payload}'::jsonb);"


def main():
    subprocess.run([
        "docker", "run", "--rm", "--detach", "--name", CONTAINER,
        "--network", "none", "--memory", "512m", "--cpus", "1", "--pids-limit", "128",
        "--tmpfs", "/var/lib/postgresql/data:rw,size=256m",
        "-e", "POSTGRES_HOST_AUTH_METHOD=trust", "postgres:17-alpine",
    ], check=True, capture_output=True)
    try:
        for _ in range(100):
            ready = subprocess.run(["docker", "exec", CONTAINER, "pg_isready", "-h", "127.0.0.1", "-U", "postgres"], capture_output=True)
            if ready.returncode == 0:
                break
            time.sleep(0.1)
        else:
            raise RuntimeError("Postgres did not start")
        sql("""
            create role anon;
            create role authenticated;
            create role service_role bypassrls;
            create table public.duel_rooms (
              id uuid primary key, created_by uuid, status text not null default 'lobby',
              total_time_sec integer, grace_after_ac_sec integer default 60,
              created_at timestamptz default now()
            );
            create table public.duel_room_players (
              room_id uuid, user_id uuid, joined_at timestamptz default now(), ready_at timestamptz,
              primary key (room_id, user_id)
            );
            grant usage on schema public to service_role;
            grant select, update on public.duel_rooms, public.duel_room_players to service_role;
        """)
        migration = (ROOT / "supabase/migrations/20261012000000_duel_problem_rating.sql").read_text()
        sql(migration)
        sql(migration)
        sql(f"insert into public.duel_rooms(id, created_by) values('{ROOM}','{A}');")
        sql(f"insert into public.duel_room_players(room_id,user_id) values('{ROOM}','{A}'),('{ROOM}','{B}');")
        assert sql(f"select problem_rating from public.duel_rooms where id='{ROOM}'") == "800"
        for role, expected in [("anon", "f"), ("authenticated", "f"), ("service_role", "t")]:
            assert sql(f"select has_function_privilege('{role}', 'public.duel_lobby_action(uuid, uuid, text, jsonb)', 'EXECUTE')") == expected
        assert json.loads(sql(action("settings", OUTSIDER, {"rating": 1600})))["status"] == 403
        assert json.loads(sql(action("settings", patch={"rating": 900})))["status"] == 400
        assert json.loads(sql(action("settings", patch={"rating": 1000})))["ok"]
        assert json.loads(sql(action("ready", patch={"ready": True, "settingsVersion": 0})))["status"] == 409
        assert not json.loads(sql(action("ready", patch={"ready": True, "settingsVersion": 1})))["claimed"]
        sql(action("settings", patch={"rating": 1000}))
        assert sql(f"select settings_version from public.duel_rooms where id='{ROOM}'") == "1"
        assert sql(f"select ready_at is not null from public.duel_room_players where user_id='{A}'") == "t"
        sql(action("settings", patch={"totalTimeSec": 600}))
        assert sql("select count(*) from public.duel_room_players where ready_at is not null") == "0"
        sql(action("ready", patch={"ready": True, "settingsVersion": 2}))
        claimed = json.loads(sql("set role service_role; " + action("ready", B, {"ready": True, "settingsVersion": 2})).splitlines()[-1])
        assert claimed["claimed"] and claimed["room"]["problem_rating"] == 1000
        assert claimed["room"]["total_time_sec"] == 600 and set(claimed["playerIds"]) == {A, B}
        assert json.loads(sql(action("settings", patch={"rating": 1600})))["status"] == 409
        assert json.loads(sql(action("ready", B, {"ready": True, "settingsVersion": 2})))["status"] == 409
        sql(action("reset"))
        assert sql("select count(*) from public.duel_room_players where ready_at is not null") == "0"

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for _ in range(20):
                sql(f"update public.duel_rooms set status='lobby', problem_rating=800, settings_version=0 where id='{ROOM}'; update public.duel_room_players set ready_at=null;")
                sql(action("ready", patch={"ready": True, "settingsVersion": 0}))
                ready = pool.submit(sql, action("ready", B, {"ready": True, "settingsVersion": 0}))
                settings = pool.submit(sql, action("settings", patch={"rating": 1600}))
                r, s = json.loads(ready.result()), json.loads(settings.result())
                state = json.loads(sql(f"select json_build_object('status',status,'rating',problem_rating,'version',settings_version) from public.duel_rooms where id='{ROOM}'"))
                if r.get("claimed"):
                    assert s["status"] == 409 and state == {"status": "racing", "rating": 800, "version": 0}
                else:
                    assert r["status"] == 409 and s["ok"] and state == {"status": "lobby", "rating": 1600, "version": 1}
                    assert sql("select count(*) from public.duel_room_players where ready_at is not null") == "0"
        print("PASS: migration idempotency, defaults, grants, membership, rating constraints, stale versions, readiness invalidation, claimed snapshot and20 concurrent ready/settings races")
    finally:
        subprocess.run(["docker", "stop", CONTAINER], check=False, capture_output=True)


if __name__ == "__main__":
    main()
