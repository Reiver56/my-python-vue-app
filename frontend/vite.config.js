// vite.config.js

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    rollupOptions: {
      // Workaround per disabilitare moduli nativi
      external: ['@rollup/rollup-linux-x64-gnu', '@rollup/rollup-linux-x64-musl'],
    }
  }
});
