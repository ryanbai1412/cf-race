"use client";

import { useEffect, useState } from "react";
import { DEFAULT_PROBLEM_RATING, DEFAULT_SOLO_TIMER, isProblemRating, isSoloTimer, type ProblemRating } from "@/lib/problem-rating";

export function usePracticeSettings(initialRating: ProblemRating = DEFAULT_PROBLEM_RATING, lockRating = false) {
  const [rating, setRating] = useState<ProblemRating>(initialRating);
  const [timerSec, setTimerSec] = useState<number>(DEFAULT_SOLO_TIMER);
  useEffect(() => {
    try {
      const savedRating = Number(localStorage.getItem("cfr-practice-rating"));
      const savedTimer = Number(localStorage.getItem("cfr-practice-timer"));
      if (!lockRating && isProblemRating(savedRating)) setRating(savedRating);
      if (isSoloTimer(savedTimer)) setTimerSec(savedTimer);
    } catch {}
  }, [lockRating]);
  const chooseRating = (value: ProblemRating) => {
    setRating(value);
    try { localStorage.setItem("cfr-practice-rating", String(value)); } catch {}
  };
  const chooseTimer = (value: number) => {
    if (!isSoloTimer(value)) return;
    setTimerSec(value);
    try { localStorage.setItem("cfr-practice-timer", String(value)); } catch {}
  };
  return { rating, timerSec, chooseRating, chooseTimer };
}
