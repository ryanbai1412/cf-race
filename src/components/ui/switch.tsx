"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

/** Minimal switch (no radix dependency): a styled toggle button. */
const Switch = React.forwardRef<
  HTMLButtonElement,
  Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "onChange"> & {
    checked: boolean;
    onCheckedChange?: (checked: boolean) => void;
  }
>(({ className, checked, onCheckedChange, disabled, ...props }, ref) => (
  <button
    type="button"
    role="switch"
    aria-checked={checked}
    ref={ref}
    disabled={disabled}
    onClick={() => onCheckedChange?.(!checked)}
    className={cn(
      "inline-flex h-5 w-9 shrink-0 items-center rounded-full border border-transparent transition-colors",
      checked ? "bg-primary" : "bg-muted",
      disabled && "cursor-not-allowed opacity-50",
      className
    )}
    {...props}
  >
    <span
      className={cn(
        "block h-4 w-4 rounded-full bg-background shadow transition-transform",
        checked ? "translate-x-4" : "translate-x-0.5"
      )}
    />
  </button>
));
Switch.displayName = "Switch";

export { Switch };
