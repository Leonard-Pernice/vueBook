import { createApp } from 'vue'
import { createPinia } from 'pinia'
// import pinia from './store/store.js'
import axios from 'axios'
import license from '@/assets/license.json'
import { registerLicense } from '@syncfusion/ej2-base'
registerLicense(license.licenses.syncfusion)

import App from './App.vue'
import router from './router'

import './assets/tailwind.css'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App)
const pinia = createPinia()

app.use(router, pinia, axios)

app.mount('#app')
