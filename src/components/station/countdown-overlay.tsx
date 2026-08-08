"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

/**
 * Full-screen 3-2-1-GO overlay driven by a server-synced start time.
 * `startAtMs` is the GO moment *and* the race-clock zero: the last second
 * before it shows "GO!", and the overlay clears exactly when the clock
 * starts, so the countdown never eats race time.
 */
export function CountdownOverlay({
  startAtMs,
  serverNow,
}: {
  startAtMs: number;
  serverNow: () => number;
}) {
  const [remaining, setRemaining] = useState(() => startAtMs - serverNow());

  useEffect(() => {
    const iv = setInterval(() => setRemaining(startAtMs - serverNow()), 100);
    return () => clearInterval(iv);
  }, [startAtMs, serverNow]);

  if (remaining <= 0) return null;
  // The final second of the countdown is the "GO!" beat.
  const secs = Math.ceil(remaining / 1000) - 1;
  const label = secs >= 1 ? String(secs) : "GO!";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur">
      <AnimatePresence mode="popLayout">
        <motion.div
          key={label}
          initial={{ scale: 2.4, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.6, opacity: 0 }}
          transition={{ duration: 0.25 }}
          className={`font-mono text-[10rem] font-black leading-none ${
            label === "GO!" ? "text-green-400" : "text-foreground"
          }`}
        >
          {label}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
