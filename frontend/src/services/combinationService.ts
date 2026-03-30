import api from './api'
import type { AxiosResponse } from 'axios'

export interface Combination {
  id: string
  name: string
  dishes: Array<{
    id: string
    name: string
    description?: string
    times_paired: number
    times_enjoyed: number
  }>
  created_at: string
}

export interface CreateCombinationRequest {
  name: string
  dish_ids: string[]
}

export interface UpdateCombinationRequest {
  name?: string
  dish_ids?: string[]
}

class CombinationService {
  async getAll(): Promise<Combination[]> {
    const response: AxiosResponse<Combination[]> = await api.get('/combinations')
    return response.data
  }

  async getById(id: string): Promise<Combination> {
    const response: AxiosResponse<Combination> = await api.get(`/combinations/${id}`)
    return response.data
  }

  async create(data: CreateCombinationRequest): Promise<Combination> {
    const response: AxiosResponse<Combination> = await api.post('/combinations', data)
    return response.data
  }

  async update(id: string, data: UpdateCombinationRequest): Promise<Combination> {
    const response: AxiosResponse<Combination> = await api.put(`/combinations/${id}`, data)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await api.delete(`/combinations/${id}`)
  }
}

export const combinationService = new CombinationService()
