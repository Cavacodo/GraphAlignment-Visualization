import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Table from '../views/Table.vue'
import OutCome from '../views/OutCome.vue'
import DeepSeek from '../views/DeepSeek.vue'
import Panel from '../views/Panel.vue'
import UserSettings from '../views/UserSettings.vue'
import editBackend from '../views/editBackend.vue'
import error from '../views/error.vue'
import editOutcome from '../views/editOutcome.vue'
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
      path: '/OutCome',
      name: 'OutCome',
      component: OutCome,
      meta: {
        requiresAuth: true
      },
    },{
      path: '/deepseek',
        name: 'DeepSeek',
        component: DeepSeek,
        meta: {
          requiresAuth: true
        }
    },{
      path: '/Panel',
      name: 'Panel',
      component: Panel,
      meta: {
        requiresAuth: true
      }
    },{
      path: '/userSettings',
      name: 'userSettings',
      component: UserSettings,
      meta: {
        requiresAuth: true
      }
    },{
      path: '/editBackend',
      name: 'editBackend',
      component: editBackend,
      meta: {
        requiresAuth: true,
        roles : ['admin']
      }
    },{
      path: '/error',
      name: 'error',
      component: error,
      meta: {
        requiresAuth: false,
        roles : ['admin','user']
      }
    },{
      path : '/editOutcome',
      name: 'editOutcome',
      component: editOutcome,
      meta: {
        requiresAuth: true,
        roles : ['admin','user']
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const token = localStorage.getItem('token');
  const userStr = localStorage.getItem('user');
  const role = localStorage.getItem('role') // 假设你在登录后存储了用户信息（包含 role）

  if (requiresAuth) {
    if (!token || !userStr) {
      // 未登录
      next({ name: 'error' });
      return;
    }

    const allowedRoles = to.meta.roles;

    if (allowedRoles && !allowedRoles.includes(role)) {
      // 用户没有访问此页面的权限
      alert("您没有权限访问该页面！");
      next({ name: 'error' }); // 阻止跳转
    } else {
      next(); // 有权限，放行
    }
  } else {
    next(); // 不需要认证的页面，直接放行
  }
});

export default router