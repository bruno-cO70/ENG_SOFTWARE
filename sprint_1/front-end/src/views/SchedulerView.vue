<script setup lang="ts">
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const { isAuthenticated, logout } = useAuth()
const router = useRouter()

function handleLogout() {
  logout()
  router.push('/')
}
</script>

<template>
  <header class="navbar">
    <a href="/" class="brand">
      <span class="brand-icon">✂</span>
      <span class="brand-name">HairTime</span>
    </a>

    <nav class="nav-links">
      <router-link to="/">Início</router-link>
      <router-link to="/beneficios">Benefícios</router-link>
      <router-link to="/sobre">Sobre</router-link>

      <template v-if="isAuthenticated">
        <router-link to="/dashboard" class="btn-nav">Dashboard</router-link>
        <button class="btn-logout" @click="handleLogout">Sair</button>
      </template>
      <template v-else>
        <router-link to="/cadastro" class="btn-nav">Entrar</router-link>
      </template>
    </nav>
  </header>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 60px;
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(8, 6, 3, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(212, 175, 55, 0.12);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.brand-icon {
  font-size: 22px;
}

.brand-name {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav-links a {
  color: #aaa;
  text-decoration: none;
  font-size: 14px;
  letter-spacing: 0.5px;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #f1c40f;
}

.btn-nav {
  padding: 9px 22px;
  border-radius: 10px;
  border: 1px solid #d4af37;
  color: #d4af37 !important;
  font-size: 14px;
  transition: background 0.2s, color 0.2s !important;
}

.btn-nav:hover {
  background: #d4af37;
  color: #000 !important;
}

.btn-logout {
  background: none;
  border: 1px solid #555;
  color: #888;
  padding: 9px 18px;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  transition: 0.2s;
  font-family: inherit;
}

.btn-logout:hover {
  border-color: #c0392b;
  color: #c0392b;
}
</style>