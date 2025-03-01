const config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        darkBackground: "var(--dark-background)",
        darkForeground: "var(--dark-foreground)",
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        dark: {
          "primary": "oklch(79% 0.209 151.711)",
          "primary-content": "oklch(26% 0.065 152.934)",
          "secondary": "oklch(84% 0.238 128.85)",
          "secondary-content": "oklch(27% 0.072 132.109)",
          "accent": "oklch(0% 0 0)",
          "accent-content": "oklch(100% 0 0)",
          "neutral": "oklch(20% 0 0)",
          "neutral-content": "oklch(98% 0 0)",
          "info": "oklch(62% 0.214 259.815)",
          "info-content": "oklch(97% 0.014 254.604)",
          "success": "oklch(69% 0.17 162.48)",
          "success-content": "oklch(97% 0.021 166.113)",
          "warning": "oklch(70% 0.213 47.604)",
          "warning-content": "oklch(98% 0.016 73.684)",
          "error": "oklch(65% 0.241 354.308)",
          "error-content": "oklch(97% 0.014 343.198)",
          "base-100": "oklch(14% 0 0)",
          "base-200": "oklch(20% 0 0)",
          "base-300": "oklch(26% 0 0)",
          "base-content": "oklch(97% 0 0)",
        },
      },
    ],
    darkTheme: "dark",
  },
};

export default config;