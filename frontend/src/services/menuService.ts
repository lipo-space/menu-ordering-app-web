import api from './api'
import type { AxiosResponse } from 'axios'
import type { Dish } from './dishService'

export interface Menu {
  id: string
  date: string
  dishes: Dish[]
  created_at: string
}

export interface MenuListResponse {
  data: Menu[]
  meta: {
    total: number
    limit: number
    offset: number
  }
}

export interface CreateMenuRequest {
  date: string
  dish_ids: string[]
}

class MenuService {
  async getAll(startDate?: string, endDate?: string, limit = 30, offset = 0): Promise<MenuListResponse> {
    const params: Record<string, any> = { limit, offset }
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate

    const response: AxiosResponse<MenuListResponse> = await api.get('/menus', { params })
    return response.data
  }

  async getToday(): Promise<Menu> {
    const response: AxiosResponse<Menu> = await api.get('/menus/today')
    return response.data
  }

  async getByDate(date: string): Promise<Menu> {
    const response: AxiosResponse<Menu> = await api.get(`/menus/${date}`)
    return response.data
  }

  async create(menu: CreateMenuRequest): Promise<Menu> {
    const response: AxiosResponse<Menu> = await api.post('/menus', menu)
    return response.data
  }

  async update(date: string, dishIds: string[]): Promise<Menu> {
    const response: AxiosResponse<Menu> = await api.put(`/menus/${date}`, { dish_ids: dishIds })
    return response.data
  }

  async delete(date: string): Promise<void> {
    await api.delete(`/menus/${date}`)
  }
}

export const menuService = new MenuService()
