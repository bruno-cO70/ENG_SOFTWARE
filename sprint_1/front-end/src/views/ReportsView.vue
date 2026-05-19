<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { relatorioService } from '@/services/api'

const loading = ref(true)
const filters = ref({ dataInicio: '', dataFim: '' })

// Estado do Relatório
const reportData = ref({
  revenue: { total: 0, currency: 'BRL' },
  appointments: { total: 0, confirmed: 0, completionRate: 0 },
  topServices: [] as any[],
  topBarbers: [] as any[]
})

onMounted(() => {
  // Por padrão, busca os últimos 30 dias se quiser, ou deixa em branco para ver tudo
  fetchReport()
})

async function fetchReport() {
  loading.value = true
  try {
    const res = await relatorioService.get({
      dataInicio: filters.value.dataInicio || undefined,
      dataFim: filters.value.dataFim || undefined
    })
    reportData.value = res.data
  } catch (error) {
    console.error("Erro ao buscar relatório", error)
  } finally {
    loading.value = false
  }
}

function exportToPDF() {
  // O CSS @media print fará a mágica de formatar a página como um documento
  window.print()
}

function clearFilters() {
  filters.value.dataInicio = ''
  filters.value.dataFim = ''
  fetchReport()
}
</script>

<template>
  <div class="page-container">
    <div class="dashboard-content print-area">
      
      <div class="header-row no-print">
        <div>
          <span class="eyebrow">Gestão</span>
          <h1 class="serif-title">Relatório <span class="gold-text">Gerencial</span></h1>
        </div>
        
        <div class="filters-container">
          <div class="date-filter">
            <input type="date" v-model="filters.dataInicio" />
            <span class="to-text">até</span>
            <input type="date" v-model="filters.dataFim" />
            <button @click="fetchReport" class="btn outline-gold small">Filtrar</button>
            <button @click="clearFilters" class="btn ghost small">Limpar</button>
          </div>
          <button @click="exportToPDF" class="btn primary-gold small">📄 Exportar PDF</button>
        </div>
      </div>

      <div class="print-only-header">
        <h1>Relatório Gerencial - HairTime</h1>
        <p>Período: {{ filters.dataInicio || 'Início' }} a {{ filters.dataFim || 'Hoje' }}</p>
      </div>

      <div v-if="loading" class="state-msg no-print">Gerando relatório...</div>
      
      <div v-else class="report-body">
        
        <div class="stats-row">
          <div class="glass-card stat-card">
            <p class="stat-label">Receita Estimada</p>
            <p class="stat-value gold-text">R$ {{ reportData.revenue.total.toFixed(2) }}</p>
          </div>
          <div class="glass-card stat-card">
            <p class="stat-label">Total de Agendamentos</p>
            <p class="stat-value">{{ reportData.appointments.total }}</p>
          </div>
          <div class="glass-card stat-card">
            <p class="stat-label">Aguardando Confirmação</p>
            <p class="stat-value">{{ reportData.appointments.confirmed }}</p>
          </div>
        </div>

        <div class="rankings-row">
          
          <div class="glass-card ranking-card">
            <h2 class="serif-title small">Serviços Mais Procurados</h2>
            <div class="list-container">
              <div v-for="(svc, index) in reportData.topServices" :key="svc.id" class="list-item">
                <span class="rank-number">{{ index + 1 }}</span>
                <span class="item-name">{{ svc.name }}</span>
                <span class="item-value">{{ svc.quantity }} realizados</span>
              </div>
              <p v-if="reportData.topServices.length === 0" class="empty-list">Nenhum dado no período.</p>
            </div>
          </div>

          <div class="glass-card ranking-card">
            <h2 class="serif-title small">Desempenho da Equipe</h2>
            <div class="list-container">
              <div v-for="(barber, index) in reportData.topBarbers" :key="barber.id" class="list-item">
                <span class="rank-number">{{ index + 1 }}</span>
                <span class="item-name">{{ barber.name }}</span>
                <span class="item-value">{{ barber.appointments }} agendamentos</span>
              </div>
              <p v-if="reportData.topBarbers.length === 0" class="empty-list">Nenhum dado no período.</p>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.page-container { min-height: 100vh; background-color: #050505; background-image: radial-gradient(circle at 50% 0%, rgba(212, 175, 55, 0.05) 0%, transparent 60%); padding: 120px 5% 60px; font-family: 'Inter', sans-serif; color: #fff; }
.dashboard-content { max-width: 1000px; margin: 0 auto; }

/* Cabeçalho e Filtros */
.header-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 24px; flex-wrap: wrap; gap: 24px; }
.eyebrow { font-size: 11px; letter-spacing: 5px; text-transform: uppercase; color: #d4af37; margin-bottom: 8px; display: block; font-weight: 600; }
.serif-title { font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 400; margin: 0; }
.serif-title.small { font-size: 22px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px;}
.gold-text { background: linear-gradient(135deg, #d4af37, #f1c40f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

.filters-container { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
.date-filter { display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.02); padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); }
.date-filter input { background: transparent; border: none; color: #fff; font-family: inherit; font-size: 13px; outline: none; color-scheme: dark; }
.to-text { font-size: 12px; color: #888; }

.glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 6px; backdrop-filter: blur(20px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }

/* KPIs */
.stats-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-bottom: 24px; }
.stat-card { padding: 32px 24px; text-align: center; }
.stat-label { color: #888; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
.stat-value { font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 600; margin: 0; }

/* Rankings */
.rankings-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; }
.ranking-card { padding: 32px; }
.list-container { display: flex; flex-direction: column; gap: 12px; }
.list-item { display: flex; align-items: center; justify-content: space-between; padding: 12px; background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); border-radius: 4px; }
.rank-number { background: #d4af37; color: #000; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 11px; font-weight: 700; }
.item-name { flex: 1; margin-left: 12px; font-size: 14px; font-weight: 500; }
.item-value { font-size: 12px; color: #aaa; background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 20px; }
.empty-list { font-size: 13px; color: #666; font-style: italic; text-align: center; margin-top: 20px; }

/* Botões */
.btn { display: inline-flex; justify-content: center; align-items: center; font-weight: 600; cursor: pointer; border: none; font-family: inherit; border-radius: 4px; transition: 0.3s; }
.btn.small { padding: 8px 16px; font-size: 12px; }
.primary-gold { background: linear-gradient(135deg, #d4af37, #f1c40f); color: #000; }
.primary-gold:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3); }
.outline-gold { background: transparent; border: 1px solid rgba(212,175,55,0.4); color: #d4af37; }
.outline-gold:hover { background: rgba(212,175,55,0.1); }
.ghost { background: transparent; color: #888; border: 1px solid transparent; }
.ghost:hover { color: #fff; }

.print-only-header { display: none; }

/* ==========================================
 * MÁGICA DA EXPORTAÇÃO PARA PDF (Impressão)
 * ========================================== */
@media print {
  /* Esconde a Navbar, Filtros, Botões e Mensagens */
  .sticky-nav, .no-print, .btn, .date-filter { display: none !important; }
  
  /* Ajusta a página para formato de documento A4 */
  @page { margin: 1cm; size: A4 portrait; }
  body { background-color: white !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  
  .page-container { background: white !important; padding: 0 !important; min-height: auto; color: black !important;}
  .dashboard-content { max-width: 100%; margin: 0; }
  
  /* Transforma os "Glass Cards" em caixas de borda limpa para o PDF */
  .glass-card { 
    background: white !important; 
    border: 1px solid #ddd !important; 
    box-shadow: none !important; 
    color: black !important;
    page-break-inside: avoid;
  }
  
  /* Cores de texto adaptadas para folha branca */
  .stat-label, .item-value, .empty-list, .to-text { color: #555 !important; }
  .gold-text, .stat-value.gold-text { color: #b8860b !important; -webkit-text-fill-color: #b8860b !important; }
  .list-item { border-color: #eee !important; background: transparent !important;}
  
  /* Mostra o cabeçalho oficial do relatório em PDF */
  .print-only-header { display: block; margin-bottom: 30px; text-align: center; border-bottom: 2px solid #b8860b; padding-bottom: 20px;}
  .print-only-header h1 { font-family: 'Playfair Display', serif; font-size: 28px; margin: 0 0 8px 0; color: #000; }
  .print-only-header p { font-size: 14px; color: #666; margin: 0;}
}
</style>