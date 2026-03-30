import { ref, computed } from 'vue'
import type { TimeSlot, Service } from '@/types'
import { availabilityService, serviceService, appointmentService } from '@/services/api'

export function useScheduler() {
  const selectedDate = ref<string>('')
  const selectedTime = ref<string | null>(null)
  const selectedServiceId = ref<string>('')
  const availableSlots = ref<TimeSlot[]>([])
  const services = ref<Service[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Por enquanto usa ID fixo; quando houver barber select, parametrize
  const BARBER_ID = 'default'

  const selectedService = computed(() =>
    services.value.find(s => s.id === selectedServiceId.value) ?? null
  )

  async function loadServices() {
    try {
      const res = await serviceService.list()
      services.value = res.data
    } catch {
      // silently fail; usa opções hardcoded como fallback
      services.value = [
        { id: '1', name: 'Corte', category: 'hair' as never, durationMinutes: 30, price: 35, active: true },
        { id: '2', name: 'Escova', category: 'hair' as never, durationMinutes: 45, price: 50, active: true },
        { id: '3', name: 'Barba', category: 'beard' as never, durationMinutes: 20, price: 25, active: true },
      ]
    }
  }

  async function onDateChange(date: string) {
    selectedDate.value = date
    selectedTime.value = null
    availableSlots.value = []

    if (!date) return

    loading.value = true
    error.value = null
    try {
      const res = await availabilityService.getSlots(BARBER_ID, date)
      availableSlots.value = res.data
    } catch {
      // fallback: gera horários locais enquanto API não está pronta
      availableSlots.value = generateLocalSlots(date)
    } finally {
      loading.value = false
    }
  }

  async function saveAppointment(): Promise<boolean> {
    if (!selectedDate.value || !selectedTime.value || !selectedServiceId.value) {
      error.value = 'Preencha todos os campos'
      return false
    }

    loading.value = true
    error.value = null
    try {
      await appointmentService.create({
        barberId: BARBER_ID,
        serviceId: selectedServiceId.value,
        date: selectedDate.value,
        time: selectedTime.value,
      })
      return true
    } catch (e: unknown) {
      error.value = (e as { message: string }).message ?? 'Erro ao agendar'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    selectedDate,
    selectedTime,
    selectedServiceId,
    availableSlots,
    services,
    selectedService,
    loading,
    error,
    loadServices,
    onDateChange,
    saveAppointment,
  }
}

// ─── FALLBACK LOCAL (enquanto API não está pronta) ───────────────────────────

function generateLocalSlots(dateStr: string): TimeSlot[] {
  const date = new Date(dateStr + 'T12:00:00')
  const day = date.getDay()

  if (day === 0) return []

  const busyTimes = new Set(['10:00', '14:30'])
  const slots: TimeSlot[] = []

  const start = day === 1 ? 10 : 9
  const end = day === 1 ? 13 : 18

  for (let h = start; h < end; h++) {
    for (const min of ['00', '30']) {
      const time = `${String(h).padStart(2, '0')}:${min}`
      slots.push({ time, available: !busyTimes.has(time) })
    }
  }

  return slots
}