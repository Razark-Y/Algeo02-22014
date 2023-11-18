/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily:{
        Merriweather:"'Merriweather',serif",
        Gillsans:"'Gill Sans MT',serif"
      }
    },
  },
  plugins: [],
}

