import MainView from "@/views/MainView";
import NavBar from "@/components/NavBar";
import Footer from "@/components/Footer";
import { navItems } from "@/_util/constants";

export default function Home() {
  return (
    <main className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <NavBar items={navItems}/>
        <MainView/>
      <Footer />
    </main>
  );
}
