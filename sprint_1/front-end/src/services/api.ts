import type {
  ApiResponse,
  ApiError,
  PaginatedResponse,
  AuthResponse,
  LoginPayload,
  RegisterPayload,
  Appointment,
  CreateAppointmentPayload,
  UpdateAppointmentPayload,
  Service,
  TimeSlot,
  User,
} from '@/types'

// ─────────────────────────────────────────────
//  CONFIG
// ─────────────────────────────────────────────

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

// ─────────────────────────────────────────────
//  HTTP CLIENT
// ─────────────────────────────────────────────

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('hairtime_token')

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      message: 'Erro inesperado',
      statusCode: response.status,
    }))
    throw error
  }

  return response.json() as Promise<T>
}

// ─────────────────────────────────────────────
//  AUTENTICAÇÃO (AUTH)
// ─────────────────────────────────────────────

export const authService = {
  login(payload: LoginPayload): Promise<ApiResponse<AuthResponse>> {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  register(payload: RegisterPayload): Promise<ApiResponse<AuthResponse>> {
    return request('/auth/cadastro', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  me(): Promise<ApiResponse<User>> {
    return request('/auth/eu')
  },

  logout(): Promise<void> {
    return request('/auth/sair', { method: 'POST' })
  },
}

// ─────────────────────────────────────────────
//  AGENDAMENTOS
// ─────────────────────────────────────────────

export const agendamentoService = {
  list(params?: {
    page?: number
    status?: string
    profissionalId?: string
  }): Promise<PaginatedResponse<Appointment>> {
    const query = new URLSearchParams(
      Object.entries(params ?? {}).filter(([, v]) => v !== undefined) as [string, string][]
    )
    return request(`/agendamentos?${query}`)
  },

  get(id: string): Promise<ApiResponse<Appointment>> {
    return request(`/agendamentos/${id}`)
  },

  create(payload: CreateAppointmentPayload): Promise<ApiResponse<Appointment>> {
    return request('/agendamentos', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  update(id: string, payload: UpdateAppointmentPayload): Promise<ApiResponse<Appointment>> {
    return request(`/agendamentos/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },

  cancel(id: string): Promise<ApiResponse<Appointment>> {
    return request(`/agendamentos/${id}/cancelar`, { method: 'PATCH' })
  },
}

// ─────────────────────────────────────────────
//  SERVIÇOS (Corte, Barba, etc)
// ─────────────────────────────────────────────

export const servicoService = {
  list(): Promise<ApiResponse<Service[]>> {
    return request('/servicos')
  },

  get(id: string): Promise<ApiResponse<Service>> {
    return request(`/servicos/${id}`)
  },
}

// ─────────────────────────────────────────────
//  DISPONIBILIDADE
// ─────────────────────────────────────────────

export const disponibilidadeService = {
  getSlots(profissionalId: string, data: string): Promise<ApiResponse<TimeSlot[]>> {
    // Usando profissional_id e data para bater com o Back-end
    return request(`/disponibilidade?profissional_id=${profissionalId}&data=${data}`)
  },
}

// ─────────────────────────────────────────────
//  PROFISSIONAIS (BARBEIROS/CABELEIREIROS)
// ─────────────────────────────────────────────

export const profissionalService = {
  list(): Promise<ApiResponse<User[]>> {
    return request('/profissionais')
  },

  get(id: string): Promise<ApiResponse<User>> {
    return request(`/profissionais/${id}`)
  },
}