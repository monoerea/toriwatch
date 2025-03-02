import PropTypes from 'prop-types';
import LayoutWrapper from "@/components/LayoutWrapper";
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
        <LayoutWrapper>
        {children}
        </LayoutWrapper>
      </body>
    </html>
  );
}
RootLayout.propTypes = {
  children: PropTypes.elementType.isRequired
};