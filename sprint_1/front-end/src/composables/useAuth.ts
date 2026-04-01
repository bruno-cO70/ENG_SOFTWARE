import { ref, computed } from 'vue'
import { authService } from '@/services/api'
import type { LoginPayload, RegisterPayload, User } from '@/types'

// Puxa do localStorage se o usuário já estava logado antes
const savedUser = localStorage.getItem('hairtime_user')
const user = ref<User | null>(savedUser ? JSON.parse(savedUser) : null)
const token = ref<string | null>(localStorage.getItem('hairtime_token'))

const loading = ref(false)
const error = ref<string | null>(null)

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials: LoginPayload) {
    loading.value = true
    error.value = null
    try {
      const res = await authService.login(credentials)
      
      // 👇 AQUI ESTÁ A CORREÇÃO: Pegando de dentro de "data"
      user.value = res.data.user
      token.value = res.data.token
      
      localStorage.setItem('hairtime_token', res.data.token)
      localStorage.setItem('hairtime_user', JSON.stringify(res.data.user))
    } catch (err: any) {
      error.value = err.message || 'Erro ao entrar'
    } finally {
      loading.value = false
    }
  }

  async function register(payload: RegisterPayload) {
    loading.value = true
    error.value = null
    try {
      const res = await authService.register(payload)
      
      // 👇 AQUI ESTÁ A CORREÇÃO TAMBÉM
      user.value = res.data.user
      token.value = res.data.token
      
      localStorage.setItem('hairtime_token', res.data.token)
      localStorage.setItem('hairtime_user', JSON.stringify(res.data.user))
    } catch (err: any) {
      error.value = err.message || 'Erro ao criar conta'
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('hairtime_token')
    localStorage.removeItem('hairtime_user')
  }

  return {
    user,
    token,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout
  }
}