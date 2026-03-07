import { defineConfig, loadEnv } from "vite"
import react from "@vitejs/plugin-react"
import fs from "fs"
import path from "path"
import { fileURLToPath } from "url"

// https://vite.dev/config/
const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "APP__")

  return {
    plugins: [
      react({
        babel: {
          plugins: [["babel-plugin-react-compiler"]],
        },
      }),
    ],
    server: env.APP__DEV === "true"
      ? {
          allowedHosts: true, // Разрешить ВСЕ хосты
          host: "0.0.0.0",
          port: 5173,
          https: {
            key: fs.readFileSync(path.resolve(__dirname, "../certs/192.168.0.101+2-key.pem")),
            cert: fs.readFileSync(path.resolve(__dirname, "../certs/192.168.0.101+2.pem")),
          },
        }
      : undefined,
    define: {
      APP__DEV: JSON.stringify(env.APP__DEV ?? "true"),
      APP__LOCAL_STACK: JSON.stringify(env.APP__LOCAL_STACK ?? "true"),
      APP__API_HOST: JSON.stringify(env.APP__API_HOST ?? "CHECK vite.config.js FOR DETAILS"),
    },
  }
})
