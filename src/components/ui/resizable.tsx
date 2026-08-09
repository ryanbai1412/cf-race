"use client";

import { Group, Panel, Separator, useDefaultLayout } from "react-resizable-panels";

import { cn } from "@/lib/utils";

/**
 * Thin wrappers over react-resizable-panels. `useResizableLayout` persists a
 * group's layout in localStorage keyed by id.
 */
function ResizablePanelGroup({
  className,
  ...props
}: React.ComponentProps<typeof Group>) {
  return <Group className={cn("min-h-0 min-w-0", className)} {...props} />;
}

const ResizablePanel = Panel;

function ResizableHandle({
  className,
  ...props
}: React.ComponentProps<typeof Separator>) {
  return (
    <Separator
      className={cn(
        "relative shrink-0 bg-border/60 transition-colors data-[state=dragging]:bg-primary/60 hover:bg-primary/40",
        className
      )}
      {...props}
    />
  );
}

function useResizableLayout(id: string) {
  return useDefaultLayout({ id, onlySaveAfterUserInteractions: true });
}

export {
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle,
  useResizableLayout,
};
