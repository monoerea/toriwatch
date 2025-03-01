"use client";
import PropTypes from "prop-types";
import Link from "next/link";

function HeroSection({ authLink }) {
  return (
    <section className="hero-content text-start max-w-md flex flex-col gap-8">
      <h1 className="text-6xl font-bold">Hello there!</h1>
      <p className="pb-2">
        ToriWatch is a free and open-source bot prediction tool for X (formerly Twitter). It helps identify and analyze bot activity with cutting-edge algorithms. Plus, it&apos;s available as a Chrome extension for seamless real-time detection while you browse.
      </p>
        <ol className="list-decimal list-inside space-y-2 text-sm">
          <li className="mb-2">
            Get started by authenticating your X account{" "}
            <code className="bg-black/[.05] dark:bg-white/[.06] px-1 py-0.5 rounded font-semibold">{authLink}</code>.
          </li>
          <li className="mb-2">
            Go to the Twitter website{" "}
            <code className="bg-black/[.05] dark:bg-white/[.06] px-1 py-0.5 rounded font-semibold">www.x.com</code>.
          </li>
        </ol>
        <div className="flex justify-center">
          <Link href="auth">
            <button className="btn btn-primary">Get Started</button>
          </Link>
        </div>
    </section>
  );
}

HeroSection.propTypes = {
  authLink: PropTypes.string.isRequired,
};

export default HeroSection;