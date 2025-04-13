import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from 'tailwindcss'

import autoprefixer from 'autoprefixer'

export default defineConfig({
  plugins: [vue()],
  server: {
  },
  css: {
    postcss: {
      plugins: [tailwindcss, autoprefixer]
    }
  }

})