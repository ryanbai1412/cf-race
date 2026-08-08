"use client";

import type { Lang } from "./types";

/**
 * The contestant's last chosen language, kept across screens so a language
 * picked before the race (solo pre-race card, warm-up sandbox) is the one the
 * race starts in — with its starter template.
 */
const KEY = "cfr-lang";

export function preferredLang(): Lang | null {
  if (typeof window === "undefined") return null;
  const v = localStorage.getItem(KEY);
  return v === "cpp" || v === "py" ? v : null;
}

export function setPreferredLang(lang: Lang) {
  if (typeof window === "undefined") return;
  localStorage.setItem(KEY, lang);
}
