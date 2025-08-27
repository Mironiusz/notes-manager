import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    watch: { usePolling: true, interval: 300 },
    hmr: { host: 'localhost', port: 5173 }
  }
})
