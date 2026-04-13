import { createRouter, createWebHistory } from 'vue-router'
import ScreenPage from '@/views/ScreenPage.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/screenpage',
      name: 'screenpage',
      component: ScreenPage,
    },
  ],
})

export default router
