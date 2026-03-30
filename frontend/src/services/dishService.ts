import api from './api'
import type { AxiosResponse } from 'axios'

export interface Dish {
  id: string
  name: string
  description?: string
  times_paired: number
  times_enjoyed: number
}

export interface DishListResponse {
  data: Dish[]
  meta: {
    total: number
    limit: number
    offset: number
  }
}

export interface CreateDishRequest {
  name: string
  description?: string
}

class DishService {
  async getAll(search?: string, limit = 50, offset = 0): Promise<DishListResponse> {
    const params: Record<string, any> = { limit, offset }
    if (search) params.search = search

    const response: AxiosResponse<DishListResponse> = await api.get('/dishes', { params })
    return response.data
  }

  async getById(id: string): Promise<Dish> {
    const response: AxiosResponse<Dish> = await api.get(`/dishes/${id}`)
    return response.data
  }

  async create(dish: CreateDishRequest): Promise<Dish> {
    const response: AxiosResponse<Dish> = await api.post('/dishes', dish)
    return response.data
  }

  async update(id: string, dish: Partial<CreateDishRequest>): Promise<Dish> {
    const response: AxiosResponse<Dish> = await api.put(`/dishes/${id}`, dish)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/dishes/${id}`)
  }
}

export const dishService = new DishService()
