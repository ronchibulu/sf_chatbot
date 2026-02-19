import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: false,
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/features/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/shared/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // UX Design System Colors (Notion-inspired)
        background: "#FFFFFF",
        surface: "#F7F7F5",
        border: "#E8E8E6",
        foreground: "#37352F",

        primary: {
          DEFAULT: "#2383E2",
          foreground: "#FFFFFF",
        },
        secondary: {
          DEFAULT: "#F7F7F5",
          foreground: "#37352F",
        },
        success: {
          DEFAULT: "#0F7B6C",
          foreground: "#FFFFFF",
        },
        warning: {
          DEFAULT: "#D9730D",
          foreground: "#FFFFFF",
        },
        destructive: {
          DEFAULT: "#E03E3E",
          foreground: "#FFFFFF",
        },
        muted: {
          DEFAULT: "#F7F7F5",
          foreground: "#9B9A97",
        },
        accent: {
          DEFAULT: "#2383E2",
          foreground: "#FFFFFF",
        },
        card: {
          DEFAULT: "#FFFFFF",
          foreground: "#37352F",
        },
        popover: {
          DEFAULT: "#FFFFFF",
          foreground: "#37352F",
        },
        input: "#E8E8E6",
        ring: "#2383E2",
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
      },
      fontSize: {
        // Typography System from UX Design
        h1: ["28px", { lineHeight: "1.5", fontWeight: "600" }],
        h2: ["22px", { lineHeight: "1.5", fontWeight: "600" }],
        h3: ["18px", { lineHeight: "1.5", fontWeight: "500" }],
        body: ["15px", { lineHeight: "1.5", fontWeight: "400" }],
        small: ["13px", { lineHeight: "1.5", fontWeight: "400" }],
        caption: ["12px", { lineHeight: "1.5", fontWeight: "400" }],
      },
      borderRadius: {
        sm: "6px",
        DEFAULT: "8px",
        md: "8px",
        lg: "12px",
        xl: "16px",
      },
      maxWidth: {
        content: "800px",
        dashboard: "1400px",
      },
      boxShadow: {
        xs: "0 1px 3px rgba(0,0,0,0.08)",
        card: "0 1px 3px rgba(0,0,0,0.08)",
        hover: "0 8px 24px rgba(0,0,0,0.12)",
      },
    },
  },
  plugins: [],
};

export default config;
