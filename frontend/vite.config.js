import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        host: '0.0.0.0', // 允许局域网设备访问前端
        port: 5173,
        proxy: {
            // 💡 只要请求以 /api 开头，就会自动转发给本机的 FastAPI (8000端口)
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true
            }
        }
    }
})
