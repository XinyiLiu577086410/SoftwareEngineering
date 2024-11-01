import { createRouter, createWebHistory } from 'vue-router'
import UserView from '../views/User.vue'
import LoginView from '../views/Login.vue'
import UserManageView from '../views/Manage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/user',
      name: 'user',
      component: UserView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/manage',
      name: 'manage',
      component: UserManageView
    },
  ]
})

export default router
