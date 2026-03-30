<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { UserType } from '@/types'

const router = useRouter()
const { login, register, loading, error } = useAuth()
const mode = ref<'login' | 'register'>('login')
const form = reactive({ name: '', email: '', password: '', confirmPassword: '', type: UserType.CLIENT })
const localError = ref<string | null>(null)

async function handleSubmit() {
  localError.value = null
  if (mode.value === 'register') {
    if (form.password !== form.confirmPassword) { localError.value = 'As senhas não coincidem'; return }
    await register({ name: form.name, email: form.email, password: form.password, type: form.type })
  } else {
    await login({ email: form.email, password: form.password })
  }
  if (!error.value) router.push('/dashboard')
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-glow" />
    <div class="auth-card">
      <div class="auth-header">
        <span class="brand-icon">✂</span>
        <h2>HairTime</h2>
        <p>{{ mode === 'login' ? 'Bem-vindo de volta' : 'Crie sua conta' }}</p>
      </div>
      <div class="tab-row">
        <button :class="{ active: mode === 'login' }" @click="mode = 'login'">Entrar</button>
        <button :class="{ active: mode === 'register' }" @click="mode = 'register'">Criar conta</button>
      </div>
      <form @submit.prevent="handleSubmit" class="auth-form">
        <div v-if="mode === 'register'" class="field">
          <label>Nome completo</label>
          <input v-model="form.name" type="text" placeholder="Seu nome" required />
        </div>
        <div class="field">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="seu@email.com" required />
        </div>
        <div class="field">
          <label>Senha</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </div>
        <template v-if="mode === 'register'">
          <div class="field">
            <label>Confirmar senha</label>
            <input v-model="form.confirmPassword" type="password" placeholder="••••••••" required />
          </div>
          <div class="field">
            <label>Tipo de conta</label>
            <select v-model="form.type">
              <option :value="UserType.CLIENT">Cliente</option>
              <option :value="UserType.BARBER">Cabeleireiro / Barbeiro</option>
            </select>
          </div>
        </template>
        <p v-if="localError || error" class="field-error">{{ localError || error }}</p>
        <button type="submit" class="submit-btn" :disabled="loading">
          <span v-if="loading">Aguarde…</span>
          <span v-else>{{ mode === 'login' ? 'Entrar' : 'Criar conta' }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.auth-page { min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px; position:relative; }
.auth-glow { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:500px; height:500px; border-radius:50%; background:radial-gradient(circle,rgba(212,175,55,0.07) 0%,transparent 70%); pointer-events:none; }
.auth-card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.09); border-radius:24px; padding:48px 44px; width:100%; max-width:440px; backdrop-filter:blur(20px); position:relative; z-index:1; }
.auth-header { text-align:center; margin-bottom:32px; }
.brand-icon { font-size:28px; display:block; margin-bottom:10px; }
.auth-header h2 { font-size:24px; font-weight:700; background:linear-gradient(135deg,#d4af37,#f1c40f); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:6px; }
.auth-header p { color:#777; font-size:14px; }
.tab-row { display:flex; background:rgba(0,0,0,0.3); border-radius:12px; padding:4px; margin-bottom:28px; }
.tab-row button { flex:1; padding:10px; border-radius:9px; border:none; background:transparent; color:#666; font-size:14px; font-family:inherit; cursor:pointer; transition:0.2s; }
.tab-row button.active { background:rgba(212,175,55,0.15); color:#f1c40f; font-weight:600; }
.auth-form { display:flex; flex-direction:column; gap:18px; }
.field { display:flex; flex-direction:column; gap:7px; }
.field label { font-size:12px; letter-spacing:0.5px; color:#888; text-transform:uppercase; }
.field input,.field select { padding:13px 16px; border-radius:12px; border:1px solid rgba(255,255,255,0.1); background:rgba(0,0,0,0.4); color:white; font-size:15px; font-family:inherit; transition:border-color 0.2s; }
.field input:focus,.field select:focus { outline:none; border-color:#d4af37; }
.field-error { color:#e74c3c; font-size:13px; text-align:center; }
.submit-btn { margin-top:8px; padding:15px; border-radius:13px; border:none; font-size:16px; font-weight:700; font-family:inherit; background:linear-gradient(135deg,#d4af37,#f1c40f); color:#000; cursor:pointer; transition:0.25s; }
.submit-btn:hover:not(:disabled) { transform:scale(1.03); box-shadow:0 0 24px rgba(212,175,55,0.4); }
.submit-btn:disabled { opacity:0.4; cursor:not-allowed; }
</style>