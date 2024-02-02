/* eslint-env node */
/** @type {import('tailwindcss').Config} */

// const plugin = require('tailwindcss/plugin')
import plugin from 'tailwindcss/plugin'

module.exports = {
  content: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'lying-s': 'url(./src/assets/img/icons/topbar1.svg)',
        'lying-knife': 'url(./src/assets/img/icons/topbar2.svg)',
        'lying-sun': 'url(./src/assets/img/icons/topbar3.svg)',
        'big-swirl': 'url(./src/assets/img/icons/narrowtop1.svg)',
        'lying-cross': 'url(./src/assets/img/icons/narrowtop2.svg)',
        'lying-x': 'url(./src/assets/img/icons/top1.svg)',
        'lying-y': 'url(./src/assets/img/icons/top2.svg)'
      },
      colors: {
        'gr-inner-blue': '#000A1C',
        'gr-outer-blue': '#001F5B'
      }
    }
  },
  plugins: [
    plugin(function ({ addUtilities }) {
      addUtilities({
        '.no-scrollbar::-webkit-scrollbar': {
          display: 'none'
        },
        '.no-scrollbar': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none'
        },
        '.border-image-source': {
          'border-image-source': 'url(./src/assets/img/icons/golden_border.png)'
        },
        '.border-image-slice': {
          'border-image-slice': '128'
        }
      })
    })
  ]
}
