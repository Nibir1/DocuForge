/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        vaisala: {
          blue: "#00a1e1",
          dark: "#0b1e2d",
        }
      }
    },
  },
  plugins: [],
}