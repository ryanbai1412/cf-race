"use client";

import { useEffect, useRef } from "react";
import {
  Room,
  RoomEvent,
  RemoteTrack,
  Track,
  createLocalVideoTrack,
} from "livekit-client";

async function getToken(eventId: string, identity: string, publish: boolean) {
  const res = await fetch("/api/livekit/token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ eventId, identity, publish }),
  });
  if (!res.ok) return null;
  return (await res.json()).token as string;
}

/** Invisible: publishes this device's webcam to the event room. */
export function WebcamPublisher({
  eventId,
  identity,
}: {
  eventId: string;
  identity: string;
}) {
  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_LIVEKIT_URL;
    if (!url) return;
    let room: Room | null = null;
    let cancelled = false;
    (async () => {
      const token = await getToken(eventId, identity, true);
      if (!token || cancelled) return;
      room = new Room();
      try {
        await room.connect(url, token);
        const track = await createLocalVideoTrack({
          resolution: { width: 640, height: 480 },
        });
        if (cancelled) {
          track.stop();
          return;
        }
        await room.localParticipant.publishTrack(track);
      } catch {
        // No camera / permission denied — webcam is best-effort.
      }
    })();
    return () => {
      cancelled = true;
      void room?.disconnect();
    };
  }, [eventId, identity]);
  return null;
}

/** Renders the webcam feed published by `publisherIdentity`. */
export function WebcamView({
  eventId,
  identity,
  publisherIdentity,
  className,
}: {
  eventId: string;
  identity: string;
  publisherIdentity: string;
  className?: string;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const url = process.env.NEXT_PUBLIC_LIVEKIT_URL;
    if (!url) return;
    let room: Room | null = null;
    let cancelled = false;

    function attach(track: RemoteTrack, participantIdentity: string) {
      if (
        participantIdentity === publisherIdentity &&
        track.kind === Track.Kind.Video &&
        videoRef.current
      ) {
        track.attach(videoRef.current);
      }
    }

    (async () => {
      const token = await getToken(eventId, identity, false);
      if (!token || cancelled) return;
      room = new Room();
      room.on(RoomEvent.TrackSubscribed, (track, _pub, participant) =>
        attach(track, participant.identity)
      );
      try {
        await room.connect(url, token);
        for (const p of room.remoteParticipants.values()) {
          for (const pub of p.trackPublications.values()) {
            if (pub.track) attach(pub.track, p.identity);
          }
        }
      } catch {}
    })();
    return () => {
      cancelled = true;
      void room?.disconnect();
    };
  }, [eventId, identity, publisherIdentity]);

  return (
    <video
      ref={videoRef}
      autoPlay
      muted
      playsInline
      className={className}
    />
  );
}
