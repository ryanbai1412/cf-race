import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";
import { RecordingUploadManager } from "@/components/recording-upload-manager";
import { ImpersonationBanner } from "@/components/shell/impersonation-banner";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Code vs Racing",
  description: "Head-to-head competitive programming races — beat your rival, beat tourist.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} flex h-dvh flex-col antialiased`}
      >
        <ImpersonationBanner />
        <div className="min-h-0 flex-1 overflow-y-auto">{children}</div>
        <Toaster />
        <RecordingUploadManager />
      </body>
    </html>
  );
}
