import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'

// Set global base URL for axios
const rawBase = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
axios.defaults.baseURL =
  (window.location.protocol === 'https:' && rawBase.startsWith('http://'))
    ? rawBase.replace('http://', 'https://')
    : rawBase;
// Bypass ngrok browser warning for free accounts
axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'true';

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
