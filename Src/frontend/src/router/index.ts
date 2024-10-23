import { createRouter, createWebHistory } from 'vue-router'
import UserView from '../views/User.vue'
import LoginView from '../views/Login.vue'

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
    // {
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})

export default router
