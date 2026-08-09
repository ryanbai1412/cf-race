import Link from "next/link";
import { Button } from "@/components/ui/button";
import { CenteredMessage } from "@/components/shell/page";

export default function InvalidLink() {
  return (
    <CenteredMessage
      eyebrow="Booth"
      title="Invalid or expired event link"
      description="Ask the organizer for a fresh device link."
    >
      <Button asChild size="sm" variant="secondary">
        <Link href="/">Back to home</Link>
      </Button>
    </CenteredMessage>
  );
}
