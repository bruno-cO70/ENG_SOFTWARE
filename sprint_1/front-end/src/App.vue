<script setup lang="ts">
import AppNavbar from '@/components/AppNavbar.vue'
</script>

<template>
  <AppNavbar />
  <main>
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </main>
</template>

<style>
/* ─── GLOBAL STYLES ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html { scroll-behavior: smooth; }

body {
  font-family: 'Outfit', sans-serif;
  background: #080603;
  color: #f0ece0;
  min-height: 100vh;
  background-image:
    radial-gradient(ellipse at 20% 0%, rgba(212, 175, 55, 0.06) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 100%, rgba(212, 175, 55, 0.04) 0%, transparent 60%);
}

/* ─── ROUTE TRANSITIONS ─────────────────────────── */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ─── SCROLLBAR ─────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: rgba(212, 175, 55, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(212, 175, 55, 0.5); }

/* ─── SELECTION ─────────────────────────────────── */
::selection { background: rgba(212, 175, 55, 0.25); color: #f1c40f; }
</style>