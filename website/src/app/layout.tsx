import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import VisitorCounter from "@/components/VisitorCounter";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Auto-News AI",
  description: "Your daily digest of trending AI tools and news, updated automatically.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100`}>
        {children}
        <footer className="text-center py-8">
          <p className="text-gray-500 dark:text-gray-400">
            Powered by Auto-News AI
          </p>
          <VisitorCounter />
        </footer>
      </body>
    </html>
  );
}
