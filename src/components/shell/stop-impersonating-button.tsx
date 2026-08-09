"use client";

import { useState } from "react";

/** Clears the impersonation cookie and reloads into the admin's own view. */
export function StopImpersonatingButton() {
  const [pending, setPending] = useState(false);
  return (
    <button
      className="rounded border border-black/30 px-2 py-0.5 text-xs font-semibold hover:bg-black/10 disabled:opacity-50"
      disabled={pending}
      onClick={async () => {
        setPending(true);
        await fetch("/api/admin/impersonate", { method: "DELETE" });
        window.location.reload();
      }}
    >
      Stop impersonating
    </button>
  );
}
