import { ref, computed, watch } from 'vue'
import type { TimeSlot, Service, User } from '@/types'
import { disponibilidadeService, servicoService, agendamentoService, profissionalService } from '@/services/api'
import { useAuth } from '@/composables/useAuth'

export function useScheduler() {
  const selectedBarberId = ref<string>('')
  const selectedDate = ref<string>('')
  const selectedTime = ref<string | null>(null)
  const selectedServiceId = ref<string>('')
  
  const professionals = ref<User[]>([])
  const availableSlots = ref<TimeSlot[]>([])
  const services = ref<Service[]>([])
  
  const loading = ref(false)
  const error = ref<string | null>(null)

  const selectedService = computed(() =>
    services.value.find(s => s.id === selectedServiceId.value) ?? null
  )

  async function loadProfessionals() {
    try {
      const res = await profissionalService.list()
      professionals.value = res.data
    } catch {
      error.value = 'Erro ao carregar profissionais'
    }
  }

  watch(selectedBarberId, async (newBarberId) => {
    selectedServiceId.value = ''
    selectedDate.value = ''
    selectedTime.value = null
    services.value = []
    availableSlots.value = []

    if (newBarberId) {
      loading.value = true
      try {
        const res = await servicoService.list()
        services.value = res.data
      } catch {
        error.value = 'Erro ao carregar serviços'
      } finally {
        loading.value = false
      }
    }
  })

  async function onDateChange(date: string) {
    selectedDate.value = date
    selectedTime.value = null
    availableSlots.value = []

    if (!date || !selectedBarberId.value) return

    loading.value = true
    error.value = null
    try {
      const res = await disponibilidadeService.getSlots(selectedBarberId.value, date)
      availableSlots.value = res.data
    } catch {
      error.value = 'Erro ao buscar horários'
    } finally {
      loading.value = false
    }
  }

  async function saveAppointment(): Promise<boolean> {
    const { user } = useAuth() // Pega os dados de quem está logado

    if (!selectedDate.value || !selectedTime.value || !selectedServiceId.value || !selectedBarberId.value) {
      error.value = 'Preencha todos os campos'
      return false
    }

    loading.value = true
    error.value = null
    try {
      await agendamentoService.create({
        barberId: selectedBarberId.value,
        serviceId: selectedServiceId.value,
        clientId: String(user.value?.id), // Envia o ID do cliente logado
        date: selectedDate.value,
        time: selectedTime.value,
      } as any)
      return true
    } catch (e: any) {
      error.value = e.message ?? 'Erro ao agendar'
      return false
    } finally {
      loading.value = false
    }
  }

  // 👇 O SEGREDO ESTAVA AQUI: Faltou devolver as variáveis pro Vue no final!
  return {
    selectedBarberId,
    selectedDate,
    selectedTime,
    selectedServiceId,
    professionals,
    availableSlots,
    services,
    selectedService,
    loading,
    error,
    loadProfessionals,
    onDateChange,
    saveAppointment,
  }
}