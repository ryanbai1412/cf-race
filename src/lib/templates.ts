import type { Lang } from "./types";

export const STARTER_TEMPLATES: Record<Lang, string> = {
  cpp: `#include <bits/stdc++.h>
using namespace std;

void solve() {
    
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t;
    cin >> t;
    while (t--) solve();
    return 0;
}
`,
  py: `import sys
input = sys.stdin.readline

def solve():
    pass

t = int(input())
for _ in range(t):
    solve()
`,
};

export function formatMs(ms: number): string {
  const total = Math.max(0, Math.floor(ms / 1000));
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function formatMsPrecise(ms: number): string {
  const total = Math.max(0, ms);
  const m = Math.floor(total / 60000);
  const s = Math.floor((total % 60000) / 1000);
  const d = Math.floor((total % 1000) / 100);
  return `${m}:${String(s).padStart(2, "0")}.${d}`;
}

/**
 * Delta between two times computed on the tenth-of-a-second values that
 * formatMsPrecise displays, so the shown time + delta always add up exactly.
 */
export function displayDeltaMs(aMs: number, bMs: number): number {
  const tenth = (ms: number) => Math.floor(Math.max(0, ms) / 100) * 100;
  return tenth(aMs) - tenth(bMs);
}
