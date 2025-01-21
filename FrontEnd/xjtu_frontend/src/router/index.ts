import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Login  // 直接将根路径指向登录页面
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})

export default router