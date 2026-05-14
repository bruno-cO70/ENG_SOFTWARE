<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { UserType } from '@/types'

const router = useRouter()
const { login, register, loading, error } = useAuth()
const mode = ref<'login' | 'register'>('login')

const form = reactive({ 
  name: '', 
  email: '', 
  password: '', 
  confirmPassword: '', 
  type: UserType.CLIENT,
  adminPassword: ''
})

const localError = ref<string | null>(null)

async function handleSubmit() {
  localError.value = null
  if (mode.value === 'register') {
    if (form.password !== form.confirmPassword) { 
      localError.value = 'As senhas não coincidem'
      return 
    }
    await register({ 
      name: form.name, 
      email: form.email, 
      password: form.password, 
      type: form.type,
      adminPassword: form.adminPassword 
    } as any)
  } else {
    await login({ email: form.email, password: form.password })
  }
  if (!error.value) router.push('/dashboard')
}
</script>

<template>
  <div class="auth-page">
    <div class="glass-card auth-card">
      
      <div class="auth-header">
        <h2 class="serif-title">Hair<span class="gold-text">Time.</span></h2>
        <p class="subtitle">{{ mode === 'login' ? 'Bem-vindo de volta' : 'Crie sua conta' }}</p>
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
          <label>E-mail</label>
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
          
          <div class="field-row">
            <div class="field">
              <label>Tipo de conta</label>
              <select v-model="form.type">
                <option :value="UserType.CLIENT">Cliente</option>
                <option :value="UserType.BARBER">Profissional</option>
              </select>
            </div>

            <transition name="fade">
              <div v-if="form.type === UserType.BARBER" class="field admin-auth">
                <label>Chave Admin</label>
                <input 
                  v-model="form.adminPassword" 
                  type="password" 
                  placeholder="Senha master" 
                  required 
                />
              </div>
            </transition>
          </div>
        </template>
        
        <p v-if="localError || error" class="field-error">{{ localError || error }}</p>
        
        <button type="submit" class="btn primary-gold submit-btn" :disabled="loading">
          <span v-if="loading">Aguarde...</span>
          <span v-else>{{ mode === 'login' ? 'Entrar no sistema' : 'Finalizar cadastro' }}</span>
        </button>
      </form>

    </div>
  </div>
</template>

<style scoped>
/* ==========================================
 * DESIGN SYSTEM: Dark & Gold High-End
 * ========================================== */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* 👇 Essa regra mágica impede que qualquer input passe de 100% de largura */
*, *::before, *::after { box-sizing: border-box; }

.auth-page { 
  min-height: 100vh; 
  background-color: #050505; 
  background-image: radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.05) 0%, transparent 60%); 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  padding: 100px 20px 40px; 
  font-family: 'Inter', sans-serif; 
}

.glass-card { 
  background: rgba(255, 255, 255, 0.02); 
  border: 1px solid rgba(255, 255, 255, 0.06); 
  border-radius: 4px; /* Pontas retas premium */
  backdrop-filter: blur(20px); 
  box-shadow: 0 30px 60px rgba(0,0,0,0.5); 
}

.auth-card { 
  width: 100%; 
  max-width: 420px; 
  padding: 40px; 
  overflow: hidden; /* Corta qualquer coisa que tente escapar */
}

.auth-header { text-align: center; margin-bottom: 24px; }
.serif-title { font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 600; margin-bottom: 4px; color: #fff; }
.gold-text { background: linear-gradient(135deg, #d4af37, #f1c40f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.subtitle { color: #888; font-size: 13px; }

.tab-row { display: flex; background: rgba(0,0,0,0.4); border-radius: 4px; padding: 4px; margin-bottom: 24px; border: 1px solid rgba(255,255,255,0.05); }
.tab-row button { flex: 1; padding: 10px; border-radius: 2px; border: none; background: transparent; color: #666; font-size: 13px; font-weight: 500; cursor: pointer; transition: 0.2s; font-family: 'Inter', sans-serif; }
.tab-row button.active { background: rgba(212,175,55,0.1); color: #d4af37; }

.auth-form { display: flex; flex-direction: column; gap: 16px; width: 100%; }
.field { display: flex; flex-direction: column; gap: 6px; width: 100%; }

/* 👇 O GRID QUE COLOCA OS CAMPOS LADO A LADO PERFEITAMENTE */
.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  width: 100%;
  align-items: end;
}

.field label { font-size: 11px; letter-spacing: 0.5px; color: #aaa; text-transform: uppercase; }
.field input, .field select { 
  width: 100%; 
  padding: 14px 16px; 
  border-radius: 4px; 
  border: 1px solid rgba(255,255,255,0.1); 
  background: rgba(0,0,0,0.3); 
  color: white; 
  font-size: 14px; 
  font-family: inherit; 
  transition: border-color 0.2s; 
  outline: none; 
  color-scheme: dark; 
}
.field input:focus, .field select:focus { border-color: #d4af37; }

/* Destaca o campo de Admin */
.admin-auth input { border-color: rgba(212,175,55,0.4); background: rgba(212,175,55,0.05); }
.admin-auth input:focus { box-shadow: 0 0 0 2px rgba(212,175,55,0.2); }

.field-error { color: #e74c3c; font-size: 13px; text-align: center; }

.btn { display: inline-flex; justify-content: center; align-items: center; padding: 14px; font-weight: 600; cursor: pointer; transition: 0.3s ease; border: none; font-family: 'Inter', sans-serif; border-radius: 4px; font-size: 15px; width: 100%; }
.primary-gold { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.primary-gold:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(212, 175, 55, 0.3); }
.primary-gold:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.submit-btn { margin-top: 8px; }

/* Animações */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s, transform 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-5px); }

/* Para celulares muito pequenos, empilha tudo para não esmagar a tela */
@media (max-width: 400px) {
  .field-row { grid-template-columns: 1fr; }
}
</style>