/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Severity colors
        severity: {
          1: '#22c55e',  // green
          2: '#eab308',  // yellow
          3: '#f97316',  // orange
          4: '#ef4444',  // red
          5: '#7f1d1d',  // dark red
        },
      },
    },
  },
  plugins: [],
}
