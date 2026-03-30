<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { appointmentService } from '@/services/api'
import type { Appointment } from '@/types'
import { AppointmentStatus } from '@/types'

const router = useRouter()
const { user, isAuthenticated, logout } = useAuth()

const appointments = ref<Appointment[]>([])
const loading = ref(true)

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.push('/cadastro')
    return
  }
  try {
    const res = await appointmentService.list()
    appointments.value = res.data
  } catch {
    // API ainda não disponível — mostra estado vazio
  } finally {
    loading.value = false
  }
})

const statusLabel: Record<AppointmentStatus, string> = {
  [AppointmentStatus.PENDING]: 'Pendente',
  [AppointmentStatus.CONFIRMED]: 'Confirmado',
  [AppointmentStatus.CANCELLED]: 'Cancelado',
  [AppointmentStatus.COMPLETED]: 'Concluído',
}

function handleLogout() {
  logout()
  router.push('/')
}
</script>

<template>
  <div class="dashboard-page">
    <div class="dash-header">
      <div>
        <p class="eyebrow">Dashboard</p>
        <h1>Olá, {{ user?.name?.split(' ')[0] }} 👋</h1>
        <p class="subtitle">{{ user?.type === 'barber' ? 'Painel do profissional' : 'Meus agendamentos' }}</p>
      </div>
      <div class="dash-actions">
        <router-link to="/agendar" class="btn primary">+ Novo agendamento</router-link>
        <button class="btn ghost" @click="handleLogout">Sair</button>
      </div>
    </div>

    <!-- STATS -->
    <div class="stats-row">
      <div class="stat-card">
        <p class="stat-value">{{ appointments.length }}</p>
        <p class="stat-label">Total</p>
      </div>
      <div class="stat-card">
        <p class="stat-value">
          {{ appointments.filter(a => a.status === AppointmentStatus.CONFIRMED).length }}
        </p>
        <p class="stat-label">Confirmados</p>
      </div>
      <div class="stat-card">
        <p class="stat-value">
          {{ appointments.filter(a => a.status === AppointmentStatus.PENDING).length }}
        </p>
        <p class="stat-label">Pendentes</p>
      </div>
    </div>

    <!-- LISTA -->
    <div class="appointments-section">
      <h2>Agendamentos</h2>

      <div v-if="loading" class="state-msg">Carregando…</div>

      <div v-else-if="appointments.length === 0" class="empty-state">
        <p>📅</p>
        <p>Nenhum agendamento ainda</p>
        <router-link to="/agendar" class="btn primary">Agendar agora</router-link>
      </div>

      <div v-else class="appointment-list">
        <div
          v-for="appt in appointments"
          :key="appt.id"
          class="appt-card"
        >
          <div class="appt-left">
            <p class="appt-date">{{ appt.date }} · {{ appt.time }}</p>
            <p class="appt-service">{{ appt.service?.name ?? 'Serviço' }}</p>
          </div>
          <span class="appt-status" :class="appt.status">
            {{ statusLabel[appt.status] }}
          </span>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.dashboard-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 60px 40px;
  min-height: 100vh;
}

.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 48px;
  gap: 20px;
  flex-wrap: wrap;
}

.eyebrow {
  font-size: 11px;
  letter-spacing: 5px;
  text-transform: uppercase;
  color: #d4af37;
  margin-bottom: 8px;
}

h1 { font-size: 38px; font-weight: 700; letter-spacing: -1px; margin-bottom: 6px; }
.subtitle { color: #666; font-size: 14px; }

.dash-actions { display: flex; gap: 12px; align-items: center; }

.btn {
  padding: 12px 24px;
  border-radius: 11px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  text-decoration: none;
  cursor: pointer;
  transition: 0.2s;
  border: none;
}

.btn.primary {
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  color: #000;
}

.btn.primary:hover { transform: scale(1.03); box-shadow: 0 0 20px rgba(212,175,55,0.4); }

.btn.ghost {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
  color: #888;
}

.btn.ghost:hover { border-color: #c0392b; color: #c0392b; }

/* STATS */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 48px;
}

.stat-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 16px;
  padding: 28px;
  text-align: center;
}

.stat-value { font-size: 40px; font-weight: 700; color: #f1c40f; }
.stat-label { color: #666; font-size: 13px; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }

/* LIST */
.appointments-section h2 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #ccc;
}

.appointment-list { display: flex; flex-direction: column; gap: 12px; }

.appt-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 20px 24px;
  transition: 0.2s;
}

.appt-card:hover { border-color: rgba(212,175,55,0.2); }

.appt-date { font-size: 13px; color: #777; margin-bottom: 4px; }
.appt-service { font-size: 16px; font-weight: 600; }

.appt-status {
  font-size: 12px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 20px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.appt-status.confirmed { background: rgba(39,174,96,0.15); color: #2ecc71; }
.appt-status.pending { background: rgba(241,196,15,0.1); color: #f1c40f; }
.appt-status.cancelled { background: rgba(231,76,60,0.1); color: #e74c3c; }
.appt-status.completed { background: rgba(255,255,255,0.06); color: #888; }

/* EMPTY */
.empty-state { text-align: center; padding: 80px 20px; color: #555; }
.empty-state p:first-child { font-size: 48px; margin-bottom: 12px; }
.empty-state p { font-size: 16px; margin-bottom: 28px; }
.state-msg { color: #555; padding: 40px 0; }
</style>