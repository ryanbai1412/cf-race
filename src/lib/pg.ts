import postgres from "postgres";

let sql: postgres.Sql | null | undefined;

/**
 * Direct Postgres connection for hot reads, bypassing PostgREST, or null when
 * DATABASE_URL isn't set. Point it at Supavisor in transaction mode (port
 * 6543): serverless instances come and go, and that pooler shares a few
 * server connections between all of them. Transaction mode can't keep
 * prepared statements, hence prepare: false. Only jsonb comes back, so skip
 * the per-connection array type lookup too.
 */
export function pg(): postgres.Sql | null {
  if (sql === undefined) {
    const url = process.env.DATABASE_URL;
    sql = url
      ? postgres(url, {
          prepare: false,
          fetch_types: false,
          max: 3,
          idle_timeout: 20,
          connect_timeout: 10,
          max_lifetime: 60 * 30,
        })
      : null;
  }
  return sql;
}
