/** Tasteful "Built by Devin" credit with the Devin wordmark. */
export function BuiltByDevin({ className }: { className?: string }) {
  return (
    <a
      href="https://devin.ai"
      target="_blank"
      rel="noopener noreferrer"
      className={
        "group inline-flex items-center gap-1.5 font-mono text-[11px] text-muted-foreground/70 transition-colors hover:text-foreground " +
        (className ?? "")
      }
    >
      built by
      <svg
        viewBox="0 0 24 24"
        aria-hidden
        className="h-3 w-3 fill-current opacity-70 transition-opacity group-hover:opacity-100"
      >
        <path d="M12 2 2 7v10l10 5 10-5V7L12 2zm0 2.2 7.5 3.75L12 11.7 4.5 7.95 12 4.2zM4 9.6l7 3.5v6.6l-7-3.5V9.6zm16 0v6.6l-7 3.5v-6.6l7-3.5z" />
      </svg>
      <span className="font-semibold">Devin</span>
    </a>
  );
}
