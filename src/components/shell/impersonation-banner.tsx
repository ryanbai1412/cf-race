import { getImpersonationState } from "@/lib/impersonation";
import { StopImpersonatingButton } from "./stop-impersonating-button";

/**
 * Persistent banner shown on every page (rendered from the root layout) while
 * an admin is viewing the app as another user.
 */
export async function ImpersonationBanner() {
  let impersonating = null;
  try {
    ({ impersonating } = await getImpersonationState());
  } catch {
    // Missing env / auth backend — never break the page over the banner.
    return null;
  }
  if (!impersonating) return null;

  return (
    <div className="sticky top-0 z-50 flex items-center justify-center gap-3 bg-amber-500 px-4 py-1.5 text-sm font-medium text-black">
      <span>
        Viewing as{" "}
        <span className="font-mono">
          {impersonating.email ?? impersonating.id}
        </span>
      </span>
      <StopImpersonatingButton />
    </div>
  );
}
