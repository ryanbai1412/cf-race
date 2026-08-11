/** Typed accessors for the events.settings jsonb blob. */
export type EventSettings = {
  requireWebcam?: boolean;
  /** Only allow races on problems with a Genna reference session (default on). */
  gennaOnly?: boolean;
};

export function requireWebcam(settings: unknown): boolean {
  return Boolean((settings as EventSettings | null)?.requireWebcam);
}

export function gennaOnly(settings: unknown): boolean {
  return (settings as EventSettings | null)?.gennaOnly !== false;
}
