import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 记得服务端改成nginx反向代理跨域
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})