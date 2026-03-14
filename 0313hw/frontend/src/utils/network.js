import axios from "axios"

export const api = axios.create({
  baseURL: import.meta.env.VITE_APP_N8N_URL || "http://localhost:8000",
  // withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})