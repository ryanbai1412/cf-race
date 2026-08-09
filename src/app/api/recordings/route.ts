import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { requireEvent } from "@/lib/event-auth";
import { raceParticipantByStation } from "@/lib/races";
import { requireSessionAccess } from "@/lib/session-auth";
import { rateLimit } from "@/lib/rate-limit";

/**
 * Webcam recordings live in the private `recordings` bucket. The webm itself
 * is uploaded straight from the browser via signed upload URLs (serverless
 * request-body limits are far too small for video).
 *
 * Streamed (default) — chunks go up while the recording is still running:
 *   POST ?step=sign&chunk=N&…            → signed URL for chunks/NNNNNN.webm
 *   POST ?step=chunk-confirm&chunk=N&size=…  → verifies the object's size
 *   POST ?step=finalize&…  { chunks:[{index,size}] }
 *        → verifies every chunk, concatenates them into the final object
 *          (WebM chunks from one MediaRecorder concatenate byte-wise),
 *          records the path in the DB, deletes the chunk objects
 *
 * Single blob (fallback for browsers without IndexedDB):
 *   POST ?step=sign&…     → { path, token }
 *   POST ?step=confirm&…  → records path/offset in the DB
 *
 * Solo/duel runs identify themselves with ?sessionId=…, event races with
 * ?eventId=…&raceId=…&station=…. offsetMs = recorder start − race/run start
 * (video time = clock − offset).
 */

export const maxDuration = 300;

const STEPS = ["sign", "confirm", "chunk-confirm", "finalize"] as const;
type Step = (typeof STEPS)[number];

/**
 * `solo/<id>.webm` → `solo/<id>/chunks/<uploadId>/000007.webm`. Chunks are
 * namespaced per upload attempt: a reload starts a new recorder whose indices
 * restart at 0, and those must not overwrite the interrupted attempt's chunks.
 * `uploadId` is empty for clients from before the namespacing.
 */
function chunkDir(path: string, uploadId: string): string {
  const base = `${path.replace(/\.webm$/, "")}/chunks`;
  return uploadId ? `${base}/${uploadId}` : base;
}

function chunkPath(path: string, uploadId: string, index: number): string {
  return `${chunkDir(path, uploadId)}/${String(index).padStart(6, "0")}.webm`;
}

export async function POST(req: NextRequest) {
  const q = req.nextUrl.searchParams;
  const step = (q.get("step") ?? "") as Step;
  const sessionId = q.get("sessionId") ?? "";
  const eventId = q.get("eventId") ?? "";
  const raceId = q.get("raceId") ?? "";
  const station = q.get("station") ?? "";
  const offsetRaw = Number(q.get("offsetMs") ?? "0");
  const offsetMs = Number.isFinite(offsetRaw) ? Math.round(offsetRaw) : 0;
  const uploadId = (q.get("upload") ?? "").replace(/[^a-zA-Z0-9-]/g, "");
  const chunkRaw = q.get("chunk");
  const chunkIndex = chunkRaw === null ? null : Number(chunkRaw);
  if (!STEPS.includes(step)) {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }
  if (
    chunkIndex !== null &&
    (!Number.isInteger(chunkIndex) || chunkIndex < 0 || chunkIndex > 100_000)
  ) {
    return NextResponse.json({ error: "bad chunk" }, { status: 400 });
  }

  // Both flows end up writing to the participant's universal session; the
  // event-race branch just resolves the session through the race + station.
  let targetSessionId: string;
  let path: string;
  if (sessionId) {
    const access = await requireSessionAccess(sessionId);
    if (!access.ok) return access.response;
    targetSessionId = access.session.id;
    path = `${access.session.kind}/${sessionId}.webm`;
  } else if (raceId && (station === "station1" || station === "station2")) {
    const event = await requireEvent(eventId);
    if (!event) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
    const found = await raceParticipantByStation(eventId, raceId, station);
    if (!found?.participant.session_id) {
      return NextResponse.json({ error: "unknown race" }, { status: 400 });
    }
    targetSessionId = found.participant.session_id;
    path = `race/${raceId}-${station}.webm`;
  } else {
    return NextResponse.json({ error: "bad request" }, { status: 400 });
  }

  // Chunked uploads sign one URL per chunk, so the ceiling has to be roomy.
  const limited = rateLimit(req, {
    name: `recordings-${step}`,
    limit: 600,
    subject: targetSessionId,
  });
  if (limited) return limited;

  if (step === "sign") {
    const target =
      chunkIndex === null ? path : chunkPath(path, uploadId, chunkIndex);
    const { data, error } = await db()
      .storage.from("recordings")
      .createSignedUploadUrl(target, { upsert: true });
    if (error || !data) {
      return NextResponse.json(
        { error: error?.message ?? "sign failed" },
        { status: 500 }
      );
    }
    return NextResponse.json({
      path: data.path,
      token: data.token,
      signedUrl: data.signedUrl,
    });
  }

  if (step === "chunk-confirm") {
    const expected = Number(q.get("size") ?? "");
    if (chunkIndex === null || !Number.isFinite(expected) || expected <= 0) {
      return NextResponse.json({ error: "bad request" }, { status: 400 });
    }
    // Storage listings lag a just-finished upload by a moment, so a first
    // miss is retried before the chunk is called lost.
    let seen: number | null = null;
    for (let attempt = 0; attempt < 3; attempt++) {
      if (attempt > 0) await new Promise((r) => setTimeout(r, 400));
      seen = await storedSize(chunkPath(path, uploadId, chunkIndex));
      if (seen === expected) return NextResponse.json({ ok: true });
    }
    console.warn(
      `[recordings] chunk ${chunkIndex} of ${path}: expected ${expected}, stored ${seen}`
    );
    return NextResponse.json(
      { error: "chunk missing or size mismatch" },
      { status: 409 }
    );
  }

  if (step === "finalize") {
    let manifest: { index: number; size: number }[];
    try {
      const body = (await req.json()) as { chunks?: { index: number; size: number }[] };
      manifest = body.chunks ?? [];
    } catch {
      return NextResponse.json({ error: "bad request" }, { status: 400 });
    }
    if (
      manifest.length === 0 ||
      manifest.some(
        (c, i) =>
          c.index !== i || !Number.isFinite(c.size) || c.size <= 0
      )
    ) {
      return NextResponse.json({ error: "bad manifest" }, { status: 400 });
    }

    // Every chunk must be present with exactly the byte size the browser
    // recorded, or the concatenation would produce a corrupt video.
    const startedAt = Date.now();
    const sizes = await storedChunkSizes(path, uploadId);
    const missing = manifest.filter((c) => sizes.get(c.index) !== c.size);
    if (missing.length > 0) {
      // A finalize that already ran deletes the chunks, so a duplicate call
      // (retry loop racing the recorder) succeeds if the stitched recording
      // is there with the manifest's total size.
      const total = manifest.reduce((n, c) => n + c.size, 0);
      if ((await storedSize(path)) === total) {
        return NextResponse.json({ ok: true, path });
      }
      console.warn(
        `[recordings] finalize ${path}: missing chunks ${missing
          .map((c) => c.index)
          .join(",")} of ${manifest.length}`
      );
      return NextResponse.json(
        { error: "chunks incomplete", missing: missing.map((c) => c.index) },
        { status: 409 }
      );
    }

    // Downloaded concurrently — stitching is dominated by per-object round
    // trips — but kept in manifest order, which is what makes the webm valid.
    const results = await Promise.all(
      manifest.map(async (c) => {
        const { data, error } = await db()
          .storage.from("recordings")
          .download(chunkPath(path, uploadId, c.index));
        if (error || !data) return { index: c.index, error: "download failed" };
        const bytes = await data.arrayBuffer();
        if (bytes.byteLength !== c.size) {
          return { index: c.index, error: "size mismatch" };
        }
        return { index: c.index, bytes };
      })
    );
    const bad = results.find((r) => r.error);
    if (bad) {
      // A concurrent finalize (another tab, or the retry loop) may have
      // deleted the chunks from under us — if it produced the recording,
      // this call succeeded too.
      const total = manifest.reduce((n, c) => n + c.size, 0);
      if ((await storedSize(path)) === total) {
        return NextResponse.json({ ok: true, path });
      }
      return NextResponse.json(
        { error: `chunk ${bad.index} ${bad.error}` },
        { status: bad.error === "size mismatch" ? 409 : 500 }
      );
    }
    const parts = results.map((r) => r.bytes as ArrayBuffer);
    const downloadedAt = Date.now();

    const { error: upErr } = await db()
      .storage.from("recordings")
      .upload(path, new Blob(parts, { type: "video/webm" }), {
        contentType: "video/webm",
        upsert: true,
      });
    if (upErr) {
      return NextResponse.json({ error: upErr.message }, { status: 500 });
    }

    const { error } = await db()
      .from("sessions")
      .update({ recording_path: path, recording_offset_ms: offsetMs })
      .eq("id", targetSessionId);
    if (error) return NextResponse.json({ error: error.message }, { status: 500 });

    console.log(
      `[recordings] finalize ${path}: ${manifest.length} chunks, download ${
        downloadedAt - startedAt
      }ms, upload ${Date.now() - downloadedAt}ms`
    );

    // Best-effort cleanup: the recording is already complete without it.
    await db()
      .storage.from("recordings")
      .remove(manifest.map((c) => chunkPath(path, uploadId, c.index)));

    return NextResponse.json({ ok: true, path });
  }

  const { error } = await db()
    .from("sessions")
    .update({ recording_path: path, recording_offset_ms: offsetMs })
    .eq("id", targetSessionId);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true, path });
}

/** Byte size of a stored object, or null when it doesn't exist. */
async function storedSize(path: string): Promise<number | null> {
  const slash = path.lastIndexOf("/");
  const dir = slash === -1 ? "" : path.slice(0, slash);
  const name = path.slice(slash + 1);
  const { data } = await db()
    .storage.from("recordings")
    .list(dir, { limit: 1, search: name });
  const size = (data?.[0]?.metadata as { size?: number } | null)?.size;
  return typeof size === "number" ? size : null;
}

/** Sizes of the chunk objects currently in storage, keyed by chunk index. */
async function storedChunkSizes(
  path: string,
  uploadId: string
): Promise<Map<number, number>> {
  const dir = chunkDir(path, uploadId);
  const sizes = new Map<number, number>();
  const pageSize = 1000;
  for (let offset = 0; ; offset += pageSize) {
    const { data, error } = await db()
      .storage.from("recordings")
      .list(dir, { limit: pageSize, offset });
    if (error || !data) break;
    for (const f of data) {
      const m = /^(\d{6})\.webm$/.exec(f.name);
      const size = (f.metadata as { size?: number } | null)?.size;
      if (m && typeof size === "number") sizes.set(Number(m[1]), size);
    }
    if (data.length < pageSize) break;
  }
  return sizes;
}
