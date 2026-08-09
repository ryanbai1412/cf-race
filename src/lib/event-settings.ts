/** Typed accessors for the events.settings jsonb blob. */
export type EventSettings = {
  requireWebcam?: boolean;
};

export function requireWebcam(settings: unknown): boolean {
  return Boolean((settings as EventSettings | null)?.requireWebcam);
}
