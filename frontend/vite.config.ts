import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Needed for Docker port mapping
    strictPort: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://backend:8000',  // Proxy to the backend service
        changeOrigin: true,
        secure: false,
      }
    }
  }
})