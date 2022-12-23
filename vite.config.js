import {defineConfig} from "vite";
const { resolve } = require('path');

export default defineConfig({
    root: './assets/source',
    build: {
        manifest: true,
        assetsDir: '',
        emptyOutDir: true,
        minify: 'esbuild',
        outDir: resolve('./assets/distribution'),
        rollupOptions: {
            input: {
                main: resolve('./assets/source/ts/index.ts'),
            },
            output: {
                chunkFileNames: undefined,
            },
        },
    },
    base: '/static/',
    publicDir: './public',
    server: {
        host: 'localhost',
        port: 3000,
        open: false,
        watch: {
          usePolling: true,
          disableGlobbing: false,
        },
    },
})
