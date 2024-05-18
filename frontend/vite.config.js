import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // 外部からのアクセスを許可
    port: 5173  // 必要に応じてポート番号を変更
  }
})
