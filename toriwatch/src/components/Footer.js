import Image from "next/image";
import { footerLinks } from "@/_util/constants";

export default function Footer() {
  return (
    <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
      {footerLinks.map(({ href, imgSrc, alt, label }) => (
        <a key={href} className="flex items-center gap-2 hover:underline" href={href} target="_blank" rel="noopener noreferrer">
          <Image aria-hidden src={imgSrc} alt={alt} width={16} height={16} />
          {label}
        </a>
      ))}
    </footer>
  );
}
