import { createApp } from 'vue'
import pinia from './store/store.js'
import axios from 'axios'

import App from './App.vue'
import router from './router'

import './assets/tailwind.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App)

app.use(router, pinia, axios)

app.mount('#app')
