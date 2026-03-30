import { ref, computed } from 'vue'
import type { User, LoginPayload, RegisterPayload } from '@/types'
import { authService } from '@/services/api'

const TOKEN_KEY = 'hairtime_token'
const USER_KEY = 'hairtime_user'

// Estado global (singleton por módulo)
const user = ref<User | null>(
  JSON.parse(localStorage.getItem(USER_KEY) ?? 'null')
)
const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
const loading = ref(false)
const error = ref<string | null>(null)

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value && !!user.value)

  async function login(payload: LoginPayload) {
    loading.value = true
    error.value = null
    try {
      const res = await authService.login(payload)
      token.value = res.data.token
      user.value = res.data.user
      localStorage.setItem(TOKEN_KEY, res.data.token)
      localStorage.setItem(USER_KEY, JSON.stringify(res.data.user))
    } catch (e: unknown) {
      error.value = (e as { message: string }).message ?? 'Erro ao fazer login'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function register(payload: RegisterPayload) {
    loading.value = true
    error.value = null
    try {
      const res = await authService.register(payload)
      token.value = res.data.token
      user.value = res.data.user
      localStorage.setItem(TOKEN_KEY, res.data.token)
      localStorage.setItem(USER_KEY, JSON.stringify(res.data.user))
    } catch (e: unknown) {
      error.value = (e as { message: string }).message ?? 'Erro ao criar conta'
      throw e
    } finally {
      loading.value = false
    }
  }

  function logout() {
    authService.logout().catch(() => {})
    token.value = null
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  }

  return { user, token, isAuthenticated, loading, error, login, register, logout }
}