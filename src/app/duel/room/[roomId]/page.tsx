import { DuelRoom } from "@/components/duel/duel-room";

export const dynamic = "force-dynamic";

export default function DuelRoomPage({
  params,
}: {
  params: { roomId: string };
}) {
  return <DuelRoom roomId={params.roomId} />;
}
