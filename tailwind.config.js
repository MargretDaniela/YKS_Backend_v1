/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        navy:  "#0D3B66",
        brand: "#1E88E5",
        gold:  "#D4AF37",
        light: "#F5F5F5",
      },
    },
  },
  plugins: [],
}