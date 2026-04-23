<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { agendamentoService, servicoService } from '@/services/api'
import type { Appointment, Service } from '@/types'
import { AppointmentStatus } from '@/types'

const router = useRouter()
const { user, isAuthenticated, logout } = useAuth()

const appointments = ref<Appointment[]>([])
const services = ref<Service[]>([])
const loading = ref(true)

// Controle de carregamento específico para o botão de cancelar
const isCanceling = ref<string | null>(null)

// Controle do formulário de serviços
const showServiceForm = ref(false)
const isCreatingService = ref(false)
const newService = reactive({ name: '', price: 0, durationMinutes: 30 })

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.push('/cadastro')
    return
  }
  await loadDashboardData()
})

async function loadDashboardData() {
  loading.value = true
  try {
    const [apptRes, servRes] = await Promise.all([
      agendamentoService.list(),
      servicoService.list()
    ])
    
    const todosAgendamentos = apptRes.data as any[]
    const now = new Date(); // Pega a data e hora exata de "agora"
    
    // 👇 NOVO FILTRO SUPER INTELIGENTE
    appointments.value = todosAgendamentos.filter(a => {
      // 1. É do usuário logado?
      const isOwner = user.value?.type === 'barber' 
        ? a.barberId === String(user.value?.id) 
        : a.clientId === String(user.value?.id);
        
      // 2. Não está cancelado?
      const isNotCancelled = a.status !== AppointmentStatus.CANCELLED;
      
      // 3. Regra dos 30 minutos: O agendamento já expirou?
      // Transforma a data do banco (2026-04-23) e hora (16:00) em um formato de tempo real
      const dataAgendamento = new Date(`${a.date}T${a.time}:00`); 
      // Adiciona 30 minutos (30 * 60.000 milissegundos) à hora do agendamento
      const limiteExpiracao = new Date(dataAgendamento.getTime() + (30 * 60000));
      
      // O agendamento só aparece se o tempo de "agora" for menor que o "limite de expiração"
      const isNotExpired = now < limiteExpiracao;

      return isOwner && isNotCancelled && isNotExpired;
    })

    services.value = servRes.data
  } catch (error) {
    console.error("Erro ao buscar dados", error)
  } finally {
    loading.value = false
  }
}

// 👇 NOVA FUNÇÃO: Conecta o botão à API de Cancelamento
async function handleCancelAppointment(id: string) {
  // Pede confirmação antes de cancelar
  if (!window.confirm("Tem certeza que deseja cancelar este agendamento? O horário será liberado.")) return;

  isCanceling.value = id; // Ativa o loading só no botão clicado
  
  try {
    await agendamentoService.cancel(id);
    // Recarrega os dados para atualizar a lista E os "cards" de estatísticas lá no topo
    await loadDashboardData(); 
  } catch (error) {
    alert("Erro ao cancelar o agendamento. Tente novamente.");
    console.error(error);
  } finally {
    isCanceling.value = null;
  }
}

async function handleAddService() {
  if (!newService.name || newService.price <= 0) return
  isCreatingService.value = true
  try {
    await servicoService.create({
      name: newService.name,
      price: newService.price,
      durationMinutes: newService.durationMinutes
    })
    showServiceForm.value = false
    newService.name = ''
    newService.price = 0
    await loadDashboardData()
  } catch (error) {
    alert("Erro ao criar serviço")
  } finally {
    isCreatingService.value = false
  }
}

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
        <h1>Olá, {{ user?.name?.split(' ')[0] || 'Profissional' }} 👋</h1>
        <p class="subtitle">{{ user?.type === 'barber' ? 'Painel do profissional' : 'Meus agendamentos' }}</p>
      </div>
      <div class="dash-actions">
        <router-link to="/agendar" class="btn primary">+ Novo agendamento</router-link>
        <button class="btn ghost" @click="handleLogout">Sair</button>
      </div>
    </div>

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

    <div v-if="user?.type === 'barber'" class="services-section">
      <div class="section-title-row">
        <h2>Meus Serviços</h2>
        <button @click="showServiceForm = !showServiceForm" class="btn outline small">
          {{ showServiceForm ? 'Cancelar' : '+ Adicionar Serviço' }}
        </button>
      </div>

      <div v-if="showServiceForm" class="service-form">
        <input v-model="newService.name" type="text" placeholder="Nome do serviço (ex: Corte Degradê)" />
        <input v-model.number="newService.price" type="number" placeholder="Preço (R$)" />
        <input v-model.number="newService.durationMinutes" type="number" placeholder="Duração (min)" />
        <button @click="handleAddService" class="btn primary" :disabled="isCreatingService">
          {{ isCreatingService ? 'Salvando...' : 'Salvar Serviço' }}
        </button>
      </div>

      <div class="services-grid">
        <div v-for="svc in services" :key="svc.id" class="service-card">
          <p class="svc-name">{{ svc.name }}</p>
          <p class="svc-details">R$ {{ svc.price.toFixed(2) }} • {{ svc.durationMinutes }} min</p>
        </div>
        <p v-if="services.length === 0" class="empty-msg">Nenhum serviço cadastrado.</p>
      </div>
    </div>

    <div class="appointments-section">
      <h2>Agenda de Clientes</h2>

      <div v-if="loading" class="state-msg">Carregando…</div>

      <div v-else-if="appointments.length === 0" class="empty-state">
        <p>📅</p>
        <p>Nenhum agendamento ainda</p>
      </div>

      <div v-else class="appointment-list">
        <div v-for="appt in appointments" :key="appt.id" class="appt-card">
          <div class="appt-left">
            <p class="appt-date">{{ appt.date }} · {{ appt.time }}</p>
            <p class="appt-service">{{ appt.service?.name || 'Serviço' }}</p>
            
            <p v-if="user?.type === 'barber'" class="appt-client">👤 Cliente: {{ (appt as any).clientName }}</p>
            <p v-else class="appt-client">✂️ Profissional: {{ (appt as any).barberName }}</p>
          </div>
          
          <div class="appt-actions">
            <span class="appt-status" :class="appt.status">
              {{ statusLabel[appt.status] }}
            </span>
            
            <button 
              v-if="appt.status !== AppointmentStatus.CANCELLED && appt.status !== AppointmentStatus.COMPLETED"
              class="btn-cancel"
              :disabled="isCanceling === appt.id"
              @click="handleCancelAppointment(appt.id)"
            >
              {{ isCanceling === appt.id ? 'Cancelando...' : 'Cancelar' }}
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.dashboard-page { max-width: 900px; margin: 0 auto; padding: 60px 40px; min-height: 100vh; }
.dash-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 48px; gap: 20px; flex-wrap: wrap; }
.eyebrow { font-size: 11px; letter-spacing: 5px; text-transform: uppercase; color: #d4af37; margin-bottom: 8px; }
h1 { font-size: 38px; font-weight: 700; letter-spacing: -1px; margin-bottom: 6px; }
.subtitle { color: #666; font-size: 14px; }
.dash-actions { display: flex; gap: 12px; align-items: center; }
.btn { padding: 12px 24px; border-radius: 11px; font-size: 14px; font-weight: 600; font-family: inherit; text-decoration: none; cursor: pointer; transition: 0.2s; border: none; }
.btn.primary { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.btn.primary:hover:not(:disabled) { transform: scale(1.03); box-shadow: 0 0 20px rgba(212,175,55,0.4); }
.btn.primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn.ghost { background: transparent; border: 1px solid rgba(255,255,255,0.12); color: #888; }
.btn.ghost:hover { border-color: #c0392b; color: #c0392b; }
.btn.outline { background: transparent; border: 1px solid rgba(212,175,55,0.5); color: #d4af37; }
.btn.outline:hover { background: rgba(212,175,55,0.1); }
.btn.small { padding: 8px 16px; font-size: 13px; border-radius: 8px; }

/* STATS */
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 48px; }
.stat-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 28px; text-align: center; }
.stat-value { font-size: 40px; font-weight: 700; color: #f1c40f; }
.stat-label { color: #666; font-size: 13px; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }

/* SERVIÇOS */
.services-section { margin-bottom: 48px; }
.section-title-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.services-section h2, .appointments-section h2 { font-size: 20px; font-weight: 600; color: #ccc;margin-bottom: 24px; }
.service-form { display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 12px; background: rgba(255,255,255,0.02); padding: 20px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; }
.service-form input { padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.5); color: white; font-family: inherit; }
.service-form input:focus { outline: none; border-color: #d4af37; }
.services-grid { display: flex; gap: 16px; flex-wrap: wrap; }
.service-card { background: rgba(212,175,55,0.05); border: 1px solid rgba(212,175,55,0.15); border-radius: 12px; padding: 16px 20px; min-width: 200px; }
.svc-name { font-weight: 600; font-size: 16px; margin-bottom: 4px; color: #fff; }
.svc-details { font-size: 13px; color: #aaa; }
.empty-msg { color: #666; font-size: 14px; font-style: italic; }

/* LISTA & AÇÕES NO CARD */
.appointment-list { display: flex; flex-direction: column; gap: 12px; }
.appt-card { display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 20px 24px; transition: 0.2s; }
.appt-card:hover { border-color: rgba(212,175,55,0.2); }
.appt-date { font-size: 13px; color: #777; margin-bottom: 4px; }
.appt-service { font-size: 16px; font-weight: 600; margin-bottom: 4px; }
.appt-client { font-size: 13px; color: #d4af37; }

/* NOVOS ESTILOS PARA O BOTÃO DE CANCELAR */
.appt-actions { display: flex; flex-direction: column; align-items: flex-end; gap: 10px; }
.btn-cancel { 
  background: transparent; 
  border: 1px solid rgba(231,76,60,0.4); 
  color: #e74c3c; 
  padding: 6px 0; 
  border-radius: 6px; 
  font-size: 11px; 
  font-weight: 600; 
  cursor: pointer; 
  text-transform: uppercase; 
  transition: 0.2s; 
  width: 120px; 
  text-align: center; 
  box-sizing: border-box;
}

.btn-cancel:hover:not(:disabled) { 
  background: rgba(231,76,60,0.1); 
  border-color: #e74c3c; 
}
.btn-cancel:disabled { 
  opacity: 0.5; 
  cursor: not-allowed; 
}

.appt-status { 
  font-size: 11px; 
  font-weight: 700; 
  padding: 6px 0; 
  border-radius: 6px; 
  letter-spacing: 0.5px; 
  text-transform: uppercase; 
  text-align: center; 
  display: inline-block;
  width: 120px; 
  box-sizing: border-box;
}

/* 👇 As novas classes em português */
.appt-status.confirmado { 
  background: rgba(39,174,96,0.1); 
  color: #2ecc71; 
  border: 1px solid rgba(39,174,96,0.3); /* Cara de botão */
}
.appt-status.pendente { 
  background: rgba(241,196,15,0.1); 
  color: #f1c40f; 
  border: 1px solid rgba(241,196,15,0.3);
}
.appt-status.Cancelado { 
  background: rgba(231,76,60,0.1); 
  color: #e74c3c; 
}
.empty-state { 
  text-align: center; 
  padding: 80px 20px; 
  color: #888; 
  background: rgba(255, 255, 255, 0.02); /* Fundo de card sutil */
  border: 1px dashed rgba(255, 255, 255, 0.15); /* Borda tracejada (estilo "vazio") */
  border-radius: 16px; 
  margin-top: 10px;
}

.empty-state p:first-child { 
  font-size: 54px; /* Emote grandão */
  margin-bottom: 16px; 
}

.empty-state p:last-child { 
  font-size: 16px; 
  font-weight: 500;
  color: #aaa;
}
</style>