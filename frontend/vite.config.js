import { defineConfig } from "vite";

export default defineConfig({
  build: {
    manifest: "manifest.json",
    outDir: "/django/static/vite/",
    emptyOutDir: true,
    rollupOptions: {
      input: "src/main.js",
    },
  },
  server: {
    host: true,
    port: 5173,
  },
});
