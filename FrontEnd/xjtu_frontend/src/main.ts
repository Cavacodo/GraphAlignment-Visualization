import './assets/main.css'
// main.ts
import "tailwindcss/tailwind.css"

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// 1. 引入 Element Plus
import ElementPlus from 'element-plus'
// 2. 引入 Element Plus 的样式
import 'element-plus/dist/index.css'
// 3. 如果需要使用中文，还需要引入中文语言包

const app = createApp(App)

app.use(ElementPlus)

app.use(router)

app.mount('#app')
