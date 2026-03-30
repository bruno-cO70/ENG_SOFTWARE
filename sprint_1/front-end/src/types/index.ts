// ─────────────────────────────────────────────
//  ENUMS
// ─────────────────────────────────────────────

export enum UserType {
  CLIENT = 'client',
  BARBER = 'barber',
  ADMIN = 'admin',
}

export enum AppointmentStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  CANCELLED = 'cancelled',
  COMPLETED = 'completed',
}

export enum ServiceCategory {
  HAIR = 'hair',
  BEARD = 'beard',
  COMBO = 'combo',
}

// ─────────────────────────────────────────────
//  MODELS
// ─────────────────────────────────────────────

export interface User {
  id: string
  name: string
  email: string
  type: UserType
  phone?: string
  avatarUrl?: string
  createdAt: string
  updatedAt: string
}

export interface Service {
  id: string
  name: string
  description?: string
  category: ServiceCategory
  durationMinutes: number
  price: number
  active: boolean
}

export interface TimeSlot {
  time: string        // "HH:MM"
  available: boolean
}

export interface Appointment {
  id: string
  clientId: string
  barberId: string
  serviceId: string
  date: string        // "YYYY-MM-DD"
  time: string        // "HH:MM"
  status: AppointmentStatus
  notes?: string
  createdAt: string
  updatedAt: string

  // Relacionamentos populados
  client?: User
  barber?: User
  service?: Service
}

// ─────────────────────────────────────────────
//  API — REQUEST PAYLOADS
// ─────────────────────────────────────────────

export interface RegisterPayload {
  name: string
  email: string
  password: string
  type: UserType
  phone?: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface CreateAppointmentPayload {
  barberId: string
  serviceId: string
  date: string
  time: string
  notes?: string
}

export interface UpdateAppointmentPayload {
  status?: AppointmentStatus
  notes?: string
}

// ─────────────────────────────────────────────
//  API — RESPONSE WRAPPERS
// ─────────────────────────────────────────────

export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface ApiError {
  message: string
  errors?: Record<string, string[]>
  statusCode: number
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  perPage: number
  totalPages: number
}

export interface AuthResponse {
  user: User
  token: string
}

// ─────────────────────────────────────────────
//  COMPOSABLE STATE TYPES
// ─────────────────────────────────────────────

export interface SchedulerState {
  selectedDate: string | null
  selectedTime: string | null
  selectedServiceId: string | null
  availableSlots: TimeSlot[]
  loading: boolean
  error: string | null
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}