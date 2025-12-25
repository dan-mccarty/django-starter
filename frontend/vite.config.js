import { defineConfig } from "vite";

export default defineConfig({
  build: {
    manifest: true,
    outDir: "../django/static/vite",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: "src/js/main.js",
      },
    },
  },
  server: {
    host: true,
    port: 5173,
  },
});
