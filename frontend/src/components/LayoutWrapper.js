"use client";
import Footer from "@/components/Footer";
import NavBar from "@/components/NavBar";
import { navItems } from "@/_util/constants";
import { usePathname } from "next/navigation";
import PropTypes from 'prop-types';

export default function LayoutWrapper({ children }) {
    const pathname = usePathname();
    const excludedPages = ["/popup"];

    if (excludedPages.includes(pathname)) {
    return <>{children}</>; // Render page without layout
    }

    return (
        <main className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-10 sm:p-10 font-[family-name:var(--font-geist-sans)]">
            <NavBar items={navItems} />
            {   children}
            <Footer />
        </main>
    );
}
LayoutWrapper.propTypes = {
    children : PropTypes.element.isRequired
}
