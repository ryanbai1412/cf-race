export function isSafeRedirectPath(value: string): boolean {
  return /^\/(?![\\/])[^\\]*$/.test(value);
}

export function safeRedirectPath(
  value: string | null | undefined,
  fallback = "/"
): string {
  return value && isSafeRedirectPath(value) ? value : fallback;
}
