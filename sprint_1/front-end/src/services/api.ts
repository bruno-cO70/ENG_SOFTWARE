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
//  AUTH
// ─────────────────────────────────────────────

export const authService = {
  login(payload: LoginPayload): Promise<ApiResponse<AuthResponse>> {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  register(payload: RegisterPayload): Promise<ApiResponse<AuthResponse>> {
    return request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  me(): Promise<ApiResponse<User>> {
    return request('/auth/me')
  },

  logout(): Promise<void> {
    return request('/auth/logout', { method: 'POST' })
  },
}

// ─────────────────────────────────────────────
//  APPOINTMENTS
// ─────────────────────────────────────────────

export const appointmentService = {
  list(params?: {
    page?: number
    status?: string
    barberId?: string
  }): Promise<PaginatedResponse<Appointment>> {
    const query = new URLSearchParams(
      Object.entries(params ?? {}).filter(([, v]) => v !== undefined) as [string, string][]
    )
    return request(`/appointments?${query}`)
  },

  get(id: string): Promise<ApiResponse<Appointment>> {
    return request(`/appointments/${id}`)
  },

  create(payload: CreateAppointmentPayload): Promise<ApiResponse<Appointment>> {
    return request('/appointments', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  update(id: string, payload: UpdateAppointmentPayload): Promise<ApiResponse<Appointment>> {
    return request(`/appointments/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },

  cancel(id: string): Promise<ApiResponse<Appointment>> {
    return request(`/appointments/${id}/cancel`, { method: 'PATCH' })
  },
}

// ─────────────────────────────────────────────
//  SERVICES
// ─────────────────────────────────────────────

export const serviceService = {
  list(): Promise<ApiResponse<Service[]>> {
    return request('/services')
  },

  get(id: string): Promise<ApiResponse<Service>> {
    return request(`/services/${id}`)
  },
}

// ─────────────────────────────────────────────
//  AVAILABILITY
// ─────────────────────────────────────────────

export const availabilityService = {
  getSlots(barberId: string, date: string): Promise<ApiResponse<TimeSlot[]>> {
    return request(`/availability?barberId=${barberId}&date=${date}`)
  },
}

// ─────────────────────────────────────────────
//  BARBERS
// ─────────────────────────────────────────────

export const barberService = {
  list(): Promise<ApiResponse<User[]>> {
    return request('/barbers')
  },

  get(id: string): Promise<ApiResponse<User>> {
    return request(`/barbers/${id}`)
  },
}