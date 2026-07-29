import { resolve } from 'node:path'
import { defineConfig } from 'vite'

export default defineConfig({
    build: {
        rolldownOptions: {
            input: {
                main: resolve(import.meta.dirname, 'index.html'),
                favorites: resolve(import.meta.dirname, 'favorites.html'),
                about: resolve(import.meta.dirname, 'about.html')
            },
        },
    },
})