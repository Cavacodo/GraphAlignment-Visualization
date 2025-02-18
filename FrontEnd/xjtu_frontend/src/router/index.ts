import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Table from '../views/Table.vue'
import Neo4j from '../views/Neo4j.vue'
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
    },
    {
      path: '/table',
      name: 'Table',
      component: Table,
      meta: {
        requiresAuth: true
      },
    },{
      path: '/neo4j',
      name: 'Neo4j',
      component: Neo4j,
      meta: {
        requiresAuth: false
      },
    }
  ]
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = localStorage.getItem('token');
  if (requiresAuth && !isAuthenticated) {
    // 如果当前路由需要认证且用户未登录，重定向到登录页面
    next({ name: 'Login' });
  } else {
    next(); // 否则继续导航
  }
});

export default router