import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  // 👇 1. SCROLL BEHAVIOR CORRIGIDO (Faz a tela deslizar até as âncoras #)
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return { el: to.hash, top:100, behavior: 'smooth' }
    } else {
      return { top: 0 }
    }
  },

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
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
    // 👇 2. ROTA DE LOGIN ADICIONADA (Para não quebrar o botão do menu)
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/CadastroView.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/servicos',
      name: 'services',
      component: () => import('@/views/ServicesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profissionais',
      name: 'professionals',
      component: () => import('@/views/ProfessionalsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/relatorios',
      name: 'reports',
      component: () => import('@/views/ReportsView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

// Guard simples — a view também redireciona, mas aqui é a camada de rota
router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('hairtime_token')
    if (!token) return { name: 'cadastro' } // Manda o usuário intruso fazer login
  }
})

export default router