import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import Antd from 'ant-design-vue'
import "mathjax/es5/tex-mml-chtml"; // 使用 tex-mml-chtml 
import "ant-design-vue/dist/reset.css";
// 1. 引入 Element Plus
import ElementPlus from 'element-plus'
// 2. 引入 Element Plus 的样式
import 'element-plus/dist/index.css'
// 3. 如果需要使用中文，还需要引入中文语言包

const app = createApp(App)

app.use(ElementPlus)

app.use(router)

app.use(Antd)
app.mount('#app')
