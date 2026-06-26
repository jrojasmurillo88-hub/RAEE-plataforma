import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import CheckinPrompt from "@/components/CheckinPrompt";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "RAEE Colombia — Dónde botar tus residuos electrónicos",
  description:
    "Encuentra el punto de recolección de RAEE más cercano en Colombia.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        {children}
        <CheckinPrompt />
      </body>
    </html>
  );
}
