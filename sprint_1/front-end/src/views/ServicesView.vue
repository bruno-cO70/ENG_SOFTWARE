<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { servicoService } from '@/services/api'
import type { Service } from '@/types'

const services = ref<Service[]>([])
const loading = ref(true)

// Controle do Modal
const isModalOpen = ref(false)
const isSaving = ref(false)
const editingId = ref<string | null>(null)

// Formulário reativo (Inicia vazio)
const form = reactive({
  name: '',
  price: null as number | null,
  durationMinutes: null as number | null
})

onMounted(() => {
  loadServices()
})

async function loadServices() {
  loading.value = true
  try {
    const res = await servicoService.list()
    services.value = res.data
  } catch (error) {
    console.error("Erro ao carregar serviços", error)
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingId.value = null
  form.name = ''
  form.price = null
  form.durationMinutes = null
  isModalOpen.value = true
}

function openEditModal(svc: Service) {
  editingId.value = svc.id
  form.name = svc.name
  form.price = svc.price
  form.durationMinutes = svc.durationMinutes
  isModalOpen.value = true
}

async function saveService() {
  if (!form.name || !form.price || !form.durationMinutes) return
  isSaving.value = true

  const payload = {
    name: form.name,
    price: Number(form.price),
    durationMinutes: Number(form.durationMinutes)
  }

  try {
    if (editingId.value) {
      await servicoService.update(editingId.value, payload)
    } else {
      await servicoService.create(payload)
    }
    isModalOpen.value = false
    await loadServices()
  } catch (error) {
    alert("Erro ao salvar serviço.")
  } finally {
    isSaving.value = false
  }
}

async function deleteService(id: string) {
  if (!window.confirm("Tem certeza que deseja excluir este serviço?")) return
  try {
    await servicoService.delete(id)
    await loadServices()
  } catch (error) {
    alert("Erro ao excluir serviço.")
  }
}
</script>

<template>
  <div class="page-container">
    <div class="dashboard-content">
      
      <div class="header-row">
        <div>
          <span class="eyebrow">Catálogo</span>
          <h1 class="serif-title">Gerenciar <span class="gold-text">Serviços</span></h1>
        </div>
        <button @click="openCreateModal" class="btn primary-gold small">+ Novo Serviço</button>
      </div>

      <div v-if="loading" class="state-msg">Carregando catálogo...</div>
      
      <div v-else-if="services.length === 0" class="glass-card empty-state">
        <span class="empty-icon">✂️</span>
        <p>Nenhum serviço cadastrado ainda.</p>
      </div>

      <div v-else class="services-grid">
        <div v-for="svc in services" :key="svc.id" class="glass-card service-card">
          <div class="svc-info">
            <h3 class="svc-name">{{ svc.name }}</h3>
            <p class="svc-details">R$ {{ svc.price.toFixed(2) }} <span class="gold-text">•</span> {{ svc.durationMinutes }} min</p>
          </div>
          <div class="svc-actions">
            <button @click="openEditModal(svc)" class="btn-edit">Editar</button>
            <button @click="deleteService(svc.id)" class="btn-delete">Excluir</button>
          </div>
        </div>
      </div>

    </div>

    <transition name="fade">
      <div v-if="isModalOpen" class="modal-overlay" @click.self="isModalOpen = false">
        <div class="glass-card modal-content">
          <h3 class="serif-title small">{{ editingId ? 'Editar Serviço' : 'Novo Serviço' }}</h3>
          <p class="modal-subtitle">Preencha os dados do procedimento abaixo.</p>

          <form @submit.prevent="saveService" class="form-grid">
            <div class="field full">
              <label>Nome do Serviço</label>
              <input v-model="form.name" type="text" placeholder="Ex: Corte Degradê" required />
            </div>
            <div class="field">
              <label>Preço (R$)</label>
              <input v-model.number="form.price" type="number" step="0.01" placeholder="0.00" required />
            </div>
            <div class="field">
              <label>Duração (min)</label>
              <input v-model.number="form.durationMinutes" type="number" placeholder="30" required />
            </div>

            <div class="modal-actions full">
              <button type="button" class="btn outline-gold small" @click="isModalOpen = false">Cancelar</button>
              <button type="submit" class="btn primary-gold small" :disabled="isSaving">
                {{ isSaving ? 'Salvando...' : 'Salvar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.page-container { min-height: 100vh; background-color: #050505; background-image: radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.05) 0%, transparent 60%); padding: 120px 5% 60px; font-family: 'Inter', sans-serif; color: #fff; }
.dashboard-content { max-width: 1000px; margin: 0 auto; }

.header-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 24px; flex-wrap: wrap; gap: 16px; }
.eyebrow { font-size: 11px; letter-spacing: 5px; text-transform: uppercase; color: #d4af37; margin-bottom: 8px; display: block; font-weight: 600; }
.serif-title { font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 400; margin: 0; }
.serif-title.small { font-size: 26px; margin-bottom: 4px; }
.gold-text { background: linear-gradient(135deg, #d4af37, #f1c40f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

.glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 4px; backdrop-filter: blur(20px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }

/* Grid de Serviços */
.services-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.service-card { padding: 24px; display: flex; flex-direction: column; justify-content: space-between; gap: 20px; transition: 0.3s; }
.service-card:hover { border-color: rgba(212,175,55,0.3); transform: translateY(-4px); }
.svc-name { font-family: 'Playfair Display', serif; font-size: 22px; margin: 0 0 8px 0; color: #fff; }
.svc-details { font-size: 13px; color: #aaa; margin: 0; }

.svc-actions { display: flex; gap: 10px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px; }
.btn-edit, .btn-delete { flex: 1; padding: 8px; border-radius: 4px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer; transition: 0.2s; background: transparent; }
.btn-edit { border: 1px solid rgba(212,175,55,0.4); color: #d4af37; }
.btn-edit:hover { background: rgba(212,175,55,0.1); }
.btn-delete { border: 1px solid rgba(231,76,60,0.4); color: #e74c3c; }
.btn-delete:hover { background: rgba(231,76,60,0.1); }

/* Modal */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(8px); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { padding: 32px; width: 90%; max-width: 440px; }
.modal-subtitle { color: #888; font-size: 13px; margin-bottom: 24px; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field.full, .modal-actions.full { grid-column: 1 / -1; }
.field label { font-size: 11px; letter-spacing: 0.5px; color: #aaa; text-transform: uppercase; }
.field input { width: 100%; padding: 12px 14px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.5); color: white; font-family: inherit; font-size: 14px; outline: none; transition: 0.2s; }
.field input:focus { border-color: #d4af37; }
.modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 8px; }

/* Botões */
.btn { display: inline-flex; justify-content: center; align-items: center; font-weight: 600; cursor: pointer; border: none; font-family: 'Inter', sans-serif; border-radius: 4px; transition: 0.3s; }
.btn.small { padding: 10px 16px; font-size: 13px; }
.primary-gold { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.primary-gold:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3); }
.outline-gold { background: transparent; border: 1px solid rgba(212,175,55,0.4); color: #d4af37; }
.outline-gold:hover { background: rgba(212,175,55,0.05); }

.empty-state { text-align: center; padding: 60px; color: #888; }
.empty-icon { font-size: 40px; margin-bottom: 16px; display: block; opacity: 0.5; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>