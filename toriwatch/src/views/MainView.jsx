import HeroSection  from "./HeroSection";

export default function MainView() {
  const authLink = "www.auth.com";

  return (
        <HeroSection authLink={authLink} />
  );
}
