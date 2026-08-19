const SAFE_REDIRECT_ORIGIN = "https://safe-redirect.invalid";
const FORBIDDEN_REDIRECT_CHARS = /[\u0000-\u001f\u007f]/;

function normalizedRedirectPath(value: string): string | null {
  if (
    !value ||
    !value.startsWith("/") ||
    value.startsWith("//") ||
    value[1] === "\\" ||
    value.includes("\\") ||
    FORBIDDEN_REDIRECT_CHARS.test(value)
  ) {
    return null;
  }

  try {
    const url = new URL(value, SAFE_REDIRECT_ORIGIN);
    if (url.origin !== SAFE_REDIRECT_ORIGIN) return null;
    return `${url.pathname}${url.search}${url.hash}`;
  } catch {
    return null;
  }
}

export function isSafeRedirectPath(value: string): boolean {
  return normalizedRedirectPath(value) !== null;
}

export function safeRedirectPath(
  value: string | null | undefined,
  fallback = "/"
): string {
  return value ? normalizedRedirectPath(value) ?? fallback : fallback;
}
