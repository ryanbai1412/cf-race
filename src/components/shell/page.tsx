import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

/**
 * Shared page furniture so every surface uses the same max-width, vertical
 * rhythm, heading scale and empty/loading treatments.
 */

export function PageShell({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return (
    <main className={cn("mx-auto w-full max-w-5xl space-y-8 px-6 py-10", className)}>
      {children}
    </main>
  );
}

export function Eyebrow({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return (
    <p
      className={cn(
        "font-mono text-xs uppercase tracking-[0.3em] text-primary",
        className
      )}
    >
      {children}
    </p>
  );
}

export function PageHeader({
  eyebrow,
  title,
  description,
  actions,
  className,
}: {
  eyebrow?: ReactNode;
  title: ReactNode;
  description?: ReactNode;
  actions?: ReactNode;
  className?: string;
}) {
  return (
    <header className={cn("flex flex-wrap items-start gap-3", className)}>
      <div className="space-y-1">
        {eyebrow && <Eyebrow>{eyebrow}</Eyebrow>}
        <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
        {description && (
          <div className="text-sm text-muted-foreground">{description}</div>
        )}
      </div>
      {actions && <div className="ml-auto flex items-center gap-2">{actions}</div>}
    </header>
  );
}

export function SectionTitle({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return (
    <h2 className={cn("text-lg font-semibold tracking-tight", className)}>
      {children}
    </h2>
  );
}

/** Inline empty state used inside list containers and cards. */
export function EmptyState({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return (
    <p
      className={cn(
        "px-4 py-8 text-center font-mono text-sm text-muted-foreground",
        className
      )}
    >
      {children}
    </p>
  );
}

/** Full-height loading state for client surfaces that own their own screen. */
export function LoadingScreen({ label = "Loading…" }: { label?: string }) {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <p className="animate-pulse font-mono text-sm text-muted-foreground">
        {label}
      </p>
    </main>
  );
}

/** Full-height message + optional action, for not-found / gated screens. */
export function CenteredMessage({
  eyebrow,
  title,
  description,
  children,
}: {
  eyebrow?: ReactNode;
  title: ReactNode;
  description?: ReactNode;
  children?: ReactNode;
}) {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 px-6 text-center">
      <div className="space-y-2">
        {eyebrow && <Eyebrow>{eyebrow}</Eyebrow>}
        <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
        {description && (
          <p className="mx-auto max-w-md text-sm text-muted-foreground">
            {description}
          </p>
        )}
      </div>
      {children && <div className="flex flex-wrap justify-center gap-2">{children}</div>}
    </main>
  );
}
