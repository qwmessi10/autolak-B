import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import axios from 'axios'

// Set global base URL for axios
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
