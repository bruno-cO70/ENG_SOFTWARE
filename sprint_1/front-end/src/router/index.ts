import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/sobre',
      name: 'sobre',
      component: () => import('@/views/SobreView.vue'),
    },
    {
      path: '/beneficios',
      name: 'beneficios',
      component: () => import('@/views/BeneficiosView.vue'),
    },
    // ----------------------------------
    {
      path: '/agendar',
      name: 'scheduler',
      component: () => import('@/views/SchedulerView.vue'),
    },
    {
      path: '/cadastro',
      name: 'cadastro',
      component: () => import('@/views/CadastroView.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

// Guard simples — a view também redireciona, mas aqui é a camada de rota
router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('hairtime_token')
    if (!token) return { name: 'cadastro' }
  }
})

export default router