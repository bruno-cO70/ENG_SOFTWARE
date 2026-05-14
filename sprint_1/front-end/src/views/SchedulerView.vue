<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useScheduler } from '@/composables/useScheduler'

const router = useRouter()
const {
  selectedBarberId,
  selectedDate,
  selectedTime,
  selectedServiceId,
  professionals,
  availableSlots,
  services,
  loading,
  error,
  loadProfessionals,
  onDateChange,
  saveAppointment,
} = useScheduler()

onMounted(async () => {
  await loadProfessionals()
})

const handleSchedule = async () => {
  const success = await saveAppointment()
  if (success) {
    alert('Agendamento realizado com sucesso!')
    router.push('/dashboard')
  }
}
</script>

<template>
  <div class="page-container">
    <div class="glass-card scheduler-card">
      <div class="scheduler-header">
        <span class="eyebrow">NOVO AGENDAMENTO</span>
        <h1 class="serif-title">Escolha seu <span class="gold-text">Horário</span></h1>
      </div>

      <div v-if="error" class="error-msg">{{ error }}</div>

      <div class="form-container">
        
        <div class="field">
          <label>1. Profissional</label>
          <select v-model="selectedBarberId" :disabled="loading">
            <option value="" disabled>Selecione quem vai te atender...</option>
            <option v-for="prof in professionals" :key="prof.id" :value="prof.id">
              {{ prof.name }}
            </option>
          </select>
        </div>

        <transition name="fade">
          <div class="field" v-if="selectedBarberId">
            <label>2. Serviço</label>
            <div v-if="services.length === 0 && loading" class="loading-msg">Carregando serviços...</div>
            <select v-else v-model="selectedServiceId" :disabled="loading">
              <option value="" disabled>Selecione o serviço...</option>
              <option v-for="svc in services" :key="svc.id" :value="svc.id">
                {{ svc.name }} ({{ svc.durationMinutes }}m) - R$ {{ svc.price.toFixed(2) }}
              </option>
            </select>
          </div>
        </transition>

        <transition name="fade">
          <div class="field" v-if="selectedServiceId">
            <label>3. Data</label>
            <input 
              type="date" 
              :value="selectedDate"
              @input="e => onDateChange((e.target as HTMLInputElement).value)"
              :min="new Date().toISOString().split('T')[0]"
              :disabled="loading"
            />
          </div>
        </transition>

        <transition name="fade">
          <div class="field" v-if="selectedDate">
            <label>4. Horário</label>
            <div v-if="loading" class="loading-msg">Buscando horários...</div>
            
            <div v-else-if="availableSlots.length > 0" class="time-grid-wrapper">
              <div class="time-grid">
                <button
                  v-for="slot in availableSlots"
                  :key="slot.time"
                  :class="['time-btn', { selected: selectedTime === slot.time, unavailable: !slot.available }]"
                  :disabled="!slot.available"
                  @click="selectedTime = slot.time"
                >
                  {{ slot.time }}
                </button>
              </div>
            </div>
            
            <div v-else class="empty-msg">Nenhum horário livre.</div>
          </div>
        </transition>

        <button 
          class="btn primary-gold submit-btn" 
          :disabled="!selectedDate || !selectedTime || !selectedServiceId || !selectedBarberId || loading"
          @click="handleSchedule"
        >
          <span v-if="loading">Processando...</span>
          <span v-else>Confirmar Agendamento</span>
        </button>

      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

.page-container {
  min-height: 100vh;
  background-color: #050505;
  background-image: radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.05) 0%, transparent 60%);
  display: flex; align-items: center; justify-content: center;
  padding: 80px 20px 20px 20px; /* Offset Navbar */
}

.glass-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 4px; backdrop-filter: blur(20px);
  box-shadow: 0 30px 60px rgba(0,0,0,0.5);
  width: 100%; max-width: 480px; 
  padding: 40px; 
  max-height: calc(100vh - 100px); /* Proteção anti-vazamento */
  overflow-y: auto;
}
.glass-card::-webkit-scrollbar { width: 4px; }
.glass-card::-webkit-scrollbar-thumb { background: rgba(212, 175, 55, 0.3); border-radius: 4px; }

.scheduler-header { text-align: center; margin-bottom: 24px; }
.eyebrow { font-size: 11px; letter-spacing: 4px; text-transform: uppercase; color: #888; margin-bottom: 8px; display: block; font-family: 'Inter', sans-serif;}
.serif-title { font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 600; margin-bottom: 4px; color: #fff; }
.gold-text { background: linear-gradient(135deg, #d4af37, #f1c40f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

.form-container { display: flex; flex-direction: column; gap: 16px; }

.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 11px; font-weight: 600; color: #aaa; text-transform: uppercase; font-family: 'Inter', sans-serif;}
.field input, .field select { padding: 14px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.3); color: white; font-size: 14px; font-family: 'Inter', sans-serif; transition: border-color 0.2s; outline: none; }
.field input:focus, .field select:focus { border-color: #d4af37; }

::-webkit-calendar-picker-indicator { filter: invert(1); opacity: 0.6; cursor: pointer; }
::-webkit-calendar-picker-indicator:hover { opacity: 1; }

/* Wrapper bloqueia o vazamento e cria scroll na grade de botões */
.time-grid-wrapper {
  max-height: 130px; 
  overflow-y: auto;
  padding-right: 4px;
}
.time-grid-wrapper::-webkit-scrollbar { width: 4px; }
.time-grid-wrapper::-webkit-scrollbar-thumb { background: rgba(212, 175, 55, 0.3); border-radius: 4px; }

.time-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }

.time-btn { background: transparent; border: 1px solid rgba(255, 255, 255, 0.15); color: #fff; padding: 10px; border-radius: 4px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif; }
.time-btn:hover:not(:disabled) { border-color: #d4af37; background: rgba(212, 175, 55, 0.05); }
.time-btn.selected { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; border-color: transparent; font-weight: 600; }
.time-btn.unavailable { border-color: rgba(255,255,255,0.05); color: #444; cursor: not-allowed; text-decoration: line-through; }

.btn { display: inline-flex; justify-content: center; align-items: center; padding: 16px; font-weight: 600; cursor: pointer; transition: 0.3s ease; border: none; font-family: 'Inter', sans-serif; border-radius: 4px; font-size: 15px; }
.primary-gold { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.primary-gold:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(212, 175, 55, 0.3); }
.primary-gold:disabled { opacity: 0.5; cursor: not-allowed; }

.submit-btn { margin-top: 10px; }
.error-msg { background: rgba(231, 76, 60, 0.1); color: #e74c3c; padding: 12px; border-radius: 4px; border: 1px solid rgba(231, 76, 60, 0.2); text-align: center; font-size: 13px;}
.empty-msg, .loading-msg { color: #888; font-size: 13px; font-style: italic; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>  