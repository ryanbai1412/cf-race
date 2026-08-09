import { Navbar } from "@/components/shell/navbar";

/** App-shell pages: persistent navbar over the page content. */
export default function ShellLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="flex h-dvh flex-col">
      <Navbar />
      <div className="min-h-0 flex-1 overflow-y-auto">{children}</div>
    </div>
  );
}
