import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path'

// GitHub Pages repo name - change this to your repo name
const repoName = 'CardiaLink'

export default defineConfig({
  plugins: [react()],
  base: process.env.NODE_ENV === 'production' ? `/${repoName}/` : '/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
