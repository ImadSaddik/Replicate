import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// axios.defaults.baseURL = 'http://localhost:8000/'
axios.defaults.baseURL = 'http://192.168.1.8:8000/'

createApp(App).use(router, axios).mount('#app')
