import PropTypes from 'prop-types';
import NavBar from "@/components/NavBar";
import Footer from "@/components/Footer";
import { navItems } from "@/_util/constants";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "ToriWatch",
  description: "Your AI-powered extension",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}
      >
        <main className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-10 sm:p-10 font-[family-name:var(--font-geist-sans)]">
        <NavBar items={navItems} />
        {children}
        <Footer />
    </main>
      </body>
    </html>
  );
}
RootLayout.propTypes = {
  children: PropTypes.elementType.isRequired
};