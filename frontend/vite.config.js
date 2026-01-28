import { defineConfig, loadEnv } from "vite"
import react from "@vitejs/plugin-react"
import fs from "fs"
import path from "path"
import { fileURLToPath } from "url"

// https://vite.dev/config/
const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "VITE_")
  const isDevServer = env.VITE_DEV === "true"

  return {
    plugins: [
      react({
        babel: {
          plugins: [["babel-plugin-react-compiler"]],
        },
      }),
    ],
    server: isDevServer
      ? {
          allowedHosts: true, // Разрешить ВСЕ хосты
          host: "0.0.0.0",
          port: 5173,
          https: {
            key: fs.readFileSync(path.resolve(__dirname, "../certs/192.168.0.108+2-key.pem")),
            cert: fs.readFileSync(path.resolve(__dirname, "../certs/192.168.0.108+2.pem")),
          },
        }
      : undefined,
    define: {
      __VITE_DEV__: JSON.stringify(env.VITE_DEV ?? "false"),
      __VITE_API_HOST__: JSON.stringify(env.VITE_API_HOST ?? "CHECK vite.config.js FOR DETAILS"),
    },
  }
})
