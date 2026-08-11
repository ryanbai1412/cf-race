/** Typed accessors for the events.settings jsonb blob. */
export type EventSettings = {
  requireWebcam?: boolean;
  selfServe?: boolean;
};

export function requireWebcam(settings: unknown): boolean {
  return Boolean((settings as EventSettings | null)?.requireWebcam);
}

/** Self-serve mode: races auto-start when both stations ready up. */
export function selfServe(settings: unknown): boolean {
  return Boolean((settings as EventSettings | null)?.selfServe);
}
