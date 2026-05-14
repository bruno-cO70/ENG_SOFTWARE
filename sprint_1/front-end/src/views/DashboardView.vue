<script setup lang="ts">
import { onMounted, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { agendamentoService, servicoService, disponibilidadeService } from '@/services/api'
import type { Appointment, Service, TimeSlot } from '@/types'
import { AppointmentStatus } from '@/types'

const router = useRouter()
const { user, isAuthenticated } = useAuth() // 👈 Removido o logout daqui, pois já está no Navbar

const appointments = ref<Appointment[]>([])
const services = ref<Service[]>([])
const loading = ref(true)

const isCanceling = ref<string | null>(null)
const showServiceForm = ref(false)
const isCreatingService = ref(false)
const newService = reactive({ 
  name: '', 
  price: null as number | null, 
  durationMinutes: null as number | null 
})

// Modal de remarcar
const rescheduleAppt = ref<Appointment | null>(null)
const rescheduleDate = ref('')
const rescheduleTime = ref('')
const rescheduleSlots = ref<TimeSlot[]>([])
const isRescheduling = ref(false)

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
    const now = new Date(); 
    
    appointments.value = todosAgendamentos.filter(a => {
      const isOwner = user.value?.type === 'barber' 
        ? a.barberId === String(user.value?.id) 
        : a.clientId === String(user.value?.id);
        
      const isNotCancelled = a.status !== AppointmentStatus.CANCELLED;
      const dataAgendamento = new Date(`${a.date}T${a.time}:00`); 
      const limiteExpiracao = new Date(dataAgendamento.getTime() + (30 * 60000));
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

async function handleCancelAppointment(id: string) {
  if (!window.confirm("Tem certeza que deseja cancelar este agendamento? O horário será liberado.")) return;
  isCanceling.value = id; 
  try {
    await agendamentoService.cancel(id);
    await loadDashboardData(); 
  } catch (error) {
    alert("Erro ao cancelar o agendamento. Tente novamente.");
  } finally {
    isCanceling.value = null;
  }
}

function openRescheduleModal(appt: Appointment) {
  rescheduleAppt.value = appt
  rescheduleDate.value = ''
  rescheduleTime.value = ''
  rescheduleSlots.value = []
}

async function fetchRescheduleSlots() {
  if (!rescheduleAppt.value || !rescheduleDate.value) return
  try {
    const res = await disponibilidadeService.getSlots(rescheduleAppt.value.barberId, rescheduleDate.value)
    rescheduleSlots.value = res.data
  } catch (error) {
    console.error("Erro ao buscar horários", error)
  }
}

async function submitReschedule() {
  if (!rescheduleAppt.value || !rescheduleDate.value || !rescheduleTime.value) return
  isRescheduling.value = true
  try {
    await agendamentoService.reschedule(rescheduleAppt.value.id, {
      date: rescheduleDate.value,
      time: rescheduleTime.value
    })
    rescheduleAppt.value = null
    await loadDashboardData()   
  } catch (error: any) {
    alert(error.message || "Erro ao remarcar. Este horário pode não estar mais disponível.")
  } finally {
    isRescheduling.value = false
  }
}

async function handleAddService() {

  if (!newService.name || !newService.price || !newService.durationMinutes) return
  
  isCreatingService.value = true
  try {
    await servicoService.create({ 
      name: newService.name, 
      price: Number(newService.price), 
      durationMinutes: Number(newService.durationMinutes) 
    })
    
    showServiceForm.value = false
    
    newService.name = ''
    newService.price = null
    newService.durationMinutes = null
    
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
</script>

<template>
  <div class="dashboard-page">
    <div class="dashboard-content">
      
      <div class="dash-header">
        <span class="eyebrow">Dashboard</span>
        <h1 class="serif-title">Olá, <span class="gold-text">{{ user?.name?.split(' ')[0] || 'Profissional' }}</span></h1>
        <p class="subtitle">{{ user?.type === 'barber' ? 'Painel de gestão da barbearia' : 'Acompanhe seus horários agendados' }}</p>
      </div>

      <div class="stats-row">
        <div class="glass-card stat-card">
          <p class="stat-value">{{ appointments.length }}</p>
          <p class="stat-label">Total</p>
        </div>
        <div class="glass-card stat-card">
          <p class="stat-value">{{ appointments.filter(a => a.status === AppointmentStatus.CONFIRMED).length }}</p>
          <p class="stat-label">Confirmados</p>
        </div>
        <div class="glass-card stat-card">
          <p class="stat-value">{{ appointments.filter(a => a.status === AppointmentStatus.PENDING).length }}</p>
          <p class="stat-label">Pendentes</p>
        </div>
      </div>

      <div v-if="user?.type === 'barber'" class="services-section">
        <div class="section-title-row">
          <h2 class="serif-title small">Meus Serviços</h2>
          <button @click="showServiceForm = !showServiceForm" class="btn outline-gold small">
            {{ showServiceForm ? 'Cancelar' : '+ Novo Serviço' }}
          </button>
        </div>

        <transition name="fade">
          <div v-if="showServiceForm" class="glass-card service-form">
            <input v-model="newService.name" type="text" placeholder="Nome do serviço" />
            <input v-model.number="newService.price" type="number" placeholder="Preço (R$)" />
            <input v-model.number="newService.durationMinutes" type="number" placeholder="Duração (min)" />
            <button @click="handleAddService" class="btn primary-gold" :disabled="isCreatingService">Salvar</button>
          </div>
        </transition>

        <div class="services-grid">
          <div v-for="svc in services" :key="svc.id" class="glass-card service-card">
            <p class="svc-name">{{ svc.name }}</p>
            <p class="svc-details">R$ {{ svc.price.toFixed(2) }} • {{ svc.durationMinutes }} min</p>
          </div>
        </div>
      </div>

      <div class="appointments-section">
        <h2 class="serif-title small">Agenda de Clientes</h2>

        <div v-if="loading" class="state-msg">Carregando seus dados...</div>
        <div v-else-if="appointments.length === 0" class="glass-card empty-state">
          <span class="empty-icon">📅</span>
          <p>Nenhum agendamento encontrado.</p>
        </div>

        <div v-else class="appointment-list">
          <div v-for="appt in appointments" :key="appt.id" class="glass-card appt-card">
            
            <div class="appt-left">
              <span class="appt-status-dot" :class="appt.status"></span>
              <div>
                <p class="appt-date">{{ appt.date }} <span class="gold-text">·</span> {{ appt.time }}</p>
                <p class="appt-service">{{ appt.service?.name || 'Serviço Padrão' }}</p>
                <p v-if="user?.type === 'barber'" class="appt-client">👤 Cliente: {{ (appt as any).clientName }}</p>
                <p v-else class="appt-client">✂️ Profissional: {{ (appt as any).barberName }}</p>
              </div>
            </div>
            
            <div class="appt-actions">
              <span class="appt-status-badge" :class="appt.status">{{ statusLabel[appt.status] }}</span>
              
              <div class="action-buttons">
                <button 
                  v-if="appt.status !== AppointmentStatus.CANCELLED && appt.status !== AppointmentStatus.COMPLETED"
                  class="btn-reschedule"
                  @click="openRescheduleModal(appt)"
                >
                  Remarcar
                </button>

                <button 
                  v-if="appt.status !== AppointmentStatus.CANCELLED && appt.status !== AppointmentStatus.COMPLETED"
                  class="btn-cancel"
                  :disabled="isCanceling === appt.id"
                  @click="handleCancelAppointment(appt.id)"
                >
                  {{ isCanceling === appt.id ? 'Aguarde...' : 'Cancelar' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <transition name="fade">
        <div v-if="rescheduleAppt" class="modal-overlay" @click.self="rescheduleAppt = null">
          <div class="glass-card modal-content">
            <h3 class="serif-title small">Remarcar Horário</h3>
            <p class="modal-subtitle">Escolha a nova data e horário disponíveis.</p>

            <input 
              type="date" 
              v-model="rescheduleDate" 
              @change="fetchRescheduleSlots" 
              class="date-input"
              :min="new Date().toISOString().split('T')[0]"
            />

            <div v-if="rescheduleSlots.length > 0" class="slots-grid">
              <button
                v-for="slot in rescheduleSlots"
                :key="slot.time"
                class="slot-btn"
                :class="{ active: rescheduleTime === slot.time }"
                :disabled="!slot.available"
                @click="rescheduleTime = slot.time"
              >
                {{ slot.time }}
              </button>
            </div>
            <p v-else-if="rescheduleDate" class="empty-msg-modal">Nenhum horário livre neste dia.</p>

            <div class="modal-actions">
              <button class="btn outline-gold small" @click="rescheduleAppt = null">Voltar</button>
              <button 
                class="btn primary-gold small" 
                :disabled="!rescheduleTime || isRescheduling"
                @click="submitReschedule"
              >
                {{ isRescheduling ? 'Salvando...' : 'Confirmar' }}
              </button>
            </div>
          </div>
        </div>
      </transition>

    </div>
  </div>
</template>

<style scoped>
/* ==========================================
 * DESIGN SYSTEM: Dark & Gold High-End (Dashboard)
 * ========================================== */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

.dashboard-page {
  min-height: 100vh;
  background-color: #050505;
  background-image: radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.05) 0%, transparent 60%);
  padding: 120px 5% 60px; /* Offset para a Navbar */
  font-family: 'Inter', sans-serif;
  color: #fff;
}

.dashboard-content {
  max-width: 1000px;
  margin: 0 auto;
}

/* Tipografia Base */
.serif-title { font-family: 'Playfair Display', serif; font-weight: 400; letter-spacing: -0.5px; margin-bottom: 8px; }
.serif-title.small { font-size: 26px; margin-bottom: 0; }
.gold-text { background: linear-gradient(135deg, #d4af37, #f1c40f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.eyebrow { font-size: 11px; letter-spacing: 5px; text-transform: uppercase; color: #d4af37; margin-bottom: 12px; display: block; font-weight: 600; }
.subtitle { color: #888; font-size: 14px; margin-bottom: 40px; }

/* Padrão Glass Card Reto (Editorial) */
.glass-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 4px;
  backdrop-filter: blur(20px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

/* Estatísticas */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 48px; }
.stat-card { padding: 32px 24px; text-align: center; transition: transform 0.3s ease; }
.stat-card:hover { border-color: rgba(212, 175, 55, 0.2); transform: translateY(-4px); }
.stat-value { font-family: 'Playfair Display', serif; font-size: 42px; color: #fff; margin-bottom: 4px; line-height: 1; }
.stat-label { color: #d4af37; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }

/* Serviços */
.services-section, .appointments-section { margin-bottom: 48px; }
.section-title-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.05); }

.service-form { display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 12px; padding: 20px; margin-bottom: 24px; border-color: rgba(212, 175, 55, 0.3); }
.service-form input { padding: 12px 16px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.4); color: white; font-family: inherit; outline: none; transition: border-color 0.2s; }
.service-form input:focus { border-color: #d4af37; }

.services-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.service-card { padding: 24px; border-color: rgba(212, 175, 55, 0.15); background: rgba(212, 175, 55, 0.02); }
.svc-name { font-weight: 600; font-size: 16px; margin-bottom: 6px; color: #fff; }
.svc-details { font-size: 13px; color: #aaa; }

/* Agendamentos */
.appointment-list { display: flex; flex-direction: column; gap: 16px; }
.appt-card { display: flex; justify-content: space-between; align-items: center; padding: 24px 32px; transition: border-color 0.3s; }
.appt-card:hover { border-color: rgba(212, 175, 55, 0.3); }

.appt-left { display: flex; align-items: flex-start; gap: 16px; }
.appt-status-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.appt-status-dot.pendente { background: #f1c40f; box-shadow: 0 0 10px rgba(241, 196, 15, 0.5); }
.appt-status-dot.confirmado { background: #2ecc71; box-shadow: 0 0 10px rgba(46, 204, 113, 0.5); }
.appt-status-dot.Cancelado { background: #e74c3c; box-shadow: 0 0 10px rgba(231, 76, 60, 0.5); }

.appt-date { font-size: 14px; font-weight: 500; color: #fff; margin-bottom: 4px; }
.appt-service { font-family: 'Playfair Display', serif; font-size: 20px; color: #ddd; margin-bottom: 6px; }
.appt-client { font-size: 13px; color: #888; }

/* ==========================================
 * AÇÕES E STATUS DOS AGENDAMENTOS (BOTÕES)
 * ========================================== */
.appt-actions { 
  display: flex; 
  flex-direction: column; 
  align-items: flex-end; 
  gap: 10px; 
}

/* 1. Etiqueta de Status (Confirmado/Pendente) */
.appt-status-badge { 
  font-size: 11px; 
  font-weight: 700; 
  text-transform: uppercase; 
  letter-spacing: 1px; 
  padding: 8px 16px;
  border-radius: 6px; 
  width: 100%; 
  text-align: center;
  box-sizing: border-box; 
}

/* Deixei as bordas um pouco mais visíveis para igualar com as de baixo */
.appt-status-badge.pendente { color: #f1c40f; background: rgba(241, 196, 15, 0.05); border: 1px solid rgba(241, 196, 15, 0.4); }
.appt-status-badge.confirmado { color: #2ecc71; background: rgba(46, 204, 113, 0.05); border: 1px solid rgba(46, 204, 113, 0.4); }
.appt-status-badge.Cancelado { color: #e74c3c; background: rgba(231, 76, 60, 0.05); border: 1px solid rgba(231, 76, 60, 0.4); } 

.action-buttons { display: flex; gap: 10px; }

.btn-cancel, .btn-reschedule { 
  background: transparent; 
  font-size: 11px; 
  font-weight: 600; 
  cursor: pointer; 
  text-transform: uppercase; 
  transition: all 0.2s ease; 
  letter-spacing: 0.5px; 
  padding: 8px 16px; 
  border-radius: 6px; 
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Remarcar (Dourado) */
.btn-reschedule { 
  color: #d4af37; 
  border: 1px solid rgba(212, 175, 55, 0.4); 
}
.btn-reschedule:hover:not(:disabled) { 
  background: rgba(212, 175, 55, 0.1); 
  border-color: #d4af37; 
}

/* Cancelar (Vermelho) */
.btn-cancel { 
  color: #e74c3c; 
  border: 1px solid rgba(231, 76, 60, 0.4); 
}
.btn-cancel:hover:not(:disabled) { 
  background: rgba(231, 76, 60, 0.1); 
  border-color: #e74c3c; 
}
.btn-cancel:disabled, .btn-reschedule:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Botões Globais */
.btn { display: inline-flex; justify-content: center; align-items: center; font-weight: 600; cursor: pointer; transition: 0.3s ease; border: none; font-family: 'Inter', sans-serif; border-radius: 4px; }
.btn.small { padding: 10px 16px; font-size: 13px; }
.btn.primary-gold { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.btn.primary-gold:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3); }
.btn.primary-gold:disabled { opacity: 0.5; cursor: not-allowed; }
.btn.outline-gold { background: transparent; color: #d4af37; border: 1px solid rgba(212,175,55,0.4); }
.btn.outline-gold:hover { background: rgba(212,175,55,0.05); border-color: #d4af37; }
.appointments-section .serif-title.small {margin-bottom: 24px; }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(8px); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { padding: 40px; width: 90%; max-width: 440px; border-color: rgba(212,175,55,0.2); }
.modal-subtitle { color: #888; font-size: 14px; margin-bottom: 24px; }
.date-input { width: 100%; padding: 14px; border-radius: 4px; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); color: white; font-family: inherit; margin-bottom: 24px; color-scheme: dark; outline: none; }
.date-input:focus { border-color: #d4af37; }
.slots-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 24px; }
.slot-btn { padding: 12px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); background: transparent; color: #fff; cursor: pointer; transition: 0.2s; font-weight: 500; }
.slot-btn:hover:not(:disabled) { border-color: #d4af37; color: #d4af37; }
.slot-btn.active { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; border-color: transparent; font-weight: 600; }
.slot-btn:disabled { opacity: 0.2; cursor: not-allowed; text-decoration: line-through; }
.empty-msg-modal { color: #e74c3c; font-size: 13px; text-align: center; margin-bottom: 20px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 12px; }

/* Animações */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Responsividade */
@media (max-width: 768px) {
  .service-form { grid-template-columns: 1fr; }
  .appt-card { flex-direction: column; align-items: flex-start; gap: 20px; }
  .appt-actions { width: 100%; flex-direction: row; justify-content: space-between; align-items: center; }
  .dash-header { text-align: center; }
}
</style>