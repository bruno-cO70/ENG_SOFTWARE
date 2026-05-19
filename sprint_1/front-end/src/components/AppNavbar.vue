<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const { isAuthenticated, user, logout } = useAuth()
const router = useRouter()

function handleLogout() {
  logout()
  router.push('/')
}
</script>

<template>
  <header class="sticky-nav">
    <div class="nav-content">
      <router-link to="/" class="logo" aria-label="Voltar para a página inicial">
        Hair<span class="gold-text">Time.</span>
      </router-link>

      <nav class="nav-links">
        <router-link to="/#sobre">Sobre Nós</router-link>
        <router-link to="/#servicos">Serviços</router-link>
        <router-link to="/#faq">FAQ</router-link>
      </nav>

      <div class="nav-actions">
        <template v-if="isAuthenticated">
          <span class="user-greeting">Olá, {{ user?.name?.split(' ')[0] }}</span>
          
          <router-link to="/dashboard" class="btn outline-gold small">Painel</router-link>
          <router-link to="/agendar" class="btn primary-gold small">Agendar</router-link>
          <button class="btn ghost-gold small" @click="handleLogout">Sair</button>
        </template>
        
        <template v-else>
          <router-link to="/login" class="btn ghost-gold small">Entrar</router-link>
          <router-link to="/agendar" class="btn primary-gold small">Agendar</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

.sticky-nav { 
  position: fixed; 
  top: 0; 
  width: 100%; 
  background: rgba(5, 5, 5, 0.9); 
  backdrop-filter: blur(16px);  
  z-index: 1000; 
  padding: 16px 5%; 
}

.nav-content { 
  max-width: 1400px; 
  margin: 0 auto; 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  flex-wrap: nowrap; /* 👈 GARANTE QUE O CONTEÚDO NUNCA QUEBRE A LINHA */
}

.logo { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 600; color: #fff; text-decoration: none; flex-shrink: 0; }
.logo span { font-weight: 400; }
.gold-text { background: linear-gradient(135deg, #d4af37, #f1c40f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

.nav-links { 
  display: flex; 
  gap: 32px; /* 👈 Reduzido de 40px para 32px para liberar espaço */
  text-transform: uppercase; 
  letter-spacing: 1px; 
  font-size: 12px; 
  white-space: nowrap;
}
.nav-links a { color: #aaa; text-decoration: none; transition: color 0.3s; }
.nav-links a:hover { color: #d4af37; }

.nav-actions { 
  display: flex; 
  align-items: center; 
  gap: 12px; /* 👈 Reduzido de 16px para 12px */
  white-space: nowrap; /* 👈 IMPEDE OS BOTÕES DE CAÍREM PARA A LINHA DE BAIXO */
  flex-shrink: 0; /* 👈 Impede a barra de ações de ser esmagada */
}

.user-greeting { color: #888; font-family: 'Inter', sans-serif; font-size: 13px; margin-right: 4px; }

.btn { display: inline-flex; justify-content: center; align-items: center; font-weight: 600; text-decoration: none; cursor: pointer; transition: all 0.3s ease; border: none; font-family: 'Inter', sans-serif; border-radius: 4px; }
.btn.small { padding: 10px 16px; font-size: 13px; min-height: 36px; }
.btn.primary-gold { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.btn.primary-gold:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3); }
.btn.outline-gold { background: transparent; color: #d4af37; border: 1px solid rgba(212,175,55,0.4); }
.btn.outline-gold:hover { border-color: #d4af37; background: rgba(212,175,55,0.05); }
.btn.ghost-gold { background: transparent; color: #aaa; }
.btn.ghost-gold:hover { color: #d4af37; }

/* Responsividade: Oculta links do meio e texto de olá em telas menores para dar espaço aos botões */
@media (max-width: 960px) { 
  .nav-links { display: none; } 
  .user-greeting { display: none; } 
}
</style>