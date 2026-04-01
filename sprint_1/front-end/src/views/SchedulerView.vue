<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useScheduler } from '@/composables/useScheduler'

const router = useRouter()
const {
  selectedDate,
  selectedTime,
  selectedServiceId,
  availableSlots,
  services,
  loading,
  error,
  loadServices,
  onDateChange,
  saveAppointment,
} = useScheduler()

onMounted(async () => {
  await loadServices()
  // Seleciona o primeiro serviço por padrão para facilitar
  if (services.value.length > 0) {
    selectedServiceId.value = services.value[0].id
  }
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
  <div class="scheduler-page">
    <div class="scheduler-card">
      <p class="eyebrow">Novo Agendamento</p>
      <h1>Escolha seu <span class="highlight">Horário</span></h1>

      <!-- MENSAGEM DE ERRO -->
      <div v-if="error" class="error-msg">{{ error }}</div>

      <div class="form-container">
        <!-- 1. SERVIÇO -->
        <div class="field">
          <label>1. Qual serviço deseja?</label>
          <select v-model="selectedServiceId" :disabled="loading">
            <option v-for="svc in services" :key="svc.id" :value="svc.id">
              {{ svc.name }} ({{ svc.durationMinutes }} min) - R$ {{ svc.price.toFixed(2) }}
            </option>
          </select>
        </div>

        <!-- 2. DATA -->
        <div class="field">
          <label>2. Escolha o dia</label>
          <input 
            type="date" 
            :value="selectedDate"
            @input="e => onDateChange((e.target as HTMLInputElement).value)"
            :min="new Date().toISOString().split('T')[0]"
            :disabled="loading"
          />
        </div>

        <!-- 3. HORÁRIO -->
        <div class="field" v-if="selectedDate">
          <label>3. Escolha o horário</label>
          <div v-if="loading" class="loading-msg">Buscando horários disponíveis...</div>
          
          <div v-else-if="availableSlots.length > 0" class="time-grid">
            <button
              v-for="slot in availableSlots"
              :key="slot.time"
              :class="['time-btn', { 
                selected: selectedTime === slot.time,
                unavailable: !slot.available 
              }]"
              :disabled="!slot.available"
              @click="selectedTime = slot.time"
            >
              {{ slot.time }}
            </button>
          </div>
          
          <div v-else class="empty-msg">
            Nenhum horário disponível nesta data.
          </div>
        </div>

        <!-- BOTÃO DE CONFIRMAR -->
        <button 
          class="submit-btn" 
          :disabled="!selectedDate || !selectedTime || !selectedServiceId || loading"
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
.scheduler-page {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  padding: 60px 20px;
}

.scheduler-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 24px;
  padding: 48px;
  width: 100%;
  max-width: 600px;
  backdrop-filter: blur(20px);
}

.eyebrow {
  font-size: 12px;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: #d4af37;
  margin-bottom: 8px;
  text-align: center;
}

h1 {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 40px;
}

.highlight {
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field label {
  font-size: 14px;
  font-weight: 600;
  color: #ccc;
}

.field input, .field select {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(0,0,0,0.4);
  color: white;
  font-size: 16px;
  font-family: inherit;
  transition: border-color 0.2s;
}

.field input:focus, .field select:focus {
  outline: none;
  border-color: #d4af37;
}

/* Color schemes for date picker calendar icon (usually black/gray by default in browsers) */
::-webkit-calendar-picker-indicator {
    filter: invert(1);
}

.time-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
}

.time-btn {
  background: transparent;
  border: 1px solid rgba(212, 175, 55, 0.5);
  color: #fff;
  padding: 14px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.time-btn:hover:not(:disabled) {
  background: rgba(212, 175, 55, 0.1);
  border-color: #f1c40f;
}

.time-btn.selected {
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  color: #000;
  border-color: transparent;
}

.time-btn.unavailable {
  border-color: rgba(255,255,255,0.1);
  color: #555;
  cursor: not-allowed;
  text-decoration: line-through;
}

.submit-btn {
  margin-top: 20px;
  padding: 18px;
  border-radius: 14px;
  border: none;
  font-size: 18px;
  font-weight: 700;
  font-family: inherit;
  background: linear-gradient(135deg, #d4af37, #f1c40f);
  color: #000;
  cursor: pointer;
  transition: 0.25s;
}

.submit-btn:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 0 24px rgba(212, 175, 55, 0.4);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #555;
  color: #888;
}

.error-msg {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(231, 76, 60, 0.2);
  text-align: center;
  font-weight: 600;
}

.empty-msg, .loading-msg {
  color: #888;
  padding: 10px 0;
  font-style: italic;
}
</style>