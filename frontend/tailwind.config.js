/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Pokemon GO inspired colors
        'pogo-blue': '#3B4CCA',
        'pogo-red': '#EE1515',
        'pogo-yellow': '#FFDE00',
        'pogo-dark': '#1A1A2E',
        'pogo-light': '#F0F3FA',
      },
    },
  },
  plugins: [],
}
