import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { menuService, type Menu } from '@/services/menuService'
import { getTodayBeijing } from '@/utils/dateUtils'

export const useMenuStore = defineStore('menus', () => {
  const todayMenu = ref<Menu | null>(null)
  const menus = ref<Menu[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const hasTodayMenu = computed(() => todayMenu.value !== null)
  const todayDishes = computed(() => todayMenu.value?.dishes || [])

  // Actions
  async function fetchTodayMenu() {
    loading.value = true
    error.value = null

    try {
      const today = getTodayBeijing()
      const menu = await menuService.getToday()
      // 只显示今天的菜单（使用北京时间）
      todayMenu.value = menu.date === today && menu.dishes && menu.dishes.length > 0 ? menu : null
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load today\'s menu'
      console.error('Failed to fetch today menu:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchMenus(startDate?: string, endDate?: string) {
    loading.value = true
    error.value = null

    try {
      const response = await menuService.getAll(startDate, endDate)
      menus.value = response.data
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load menus'
      console.error('Failed to fetch menus:', e)
    } finally {
      loading.value = false
    }
  }

  async function createMenu(date: string, dishIds: string[]) {
    loading.value = true
    error.value = null

    try {
      const newMenu = await menuService.create({ date, dish_ids: dishIds })
      // 更新今日菜单（使用北京时间）
      const today = getTodayBeijing()
      if (date === today) {
        todayMenu.value = newMenu
      }
      // 更新菜单列表
      const existingIndex = menus.value.findIndex(m => m.date === date)
      if (existingIndex > -1) {
        menus.value[existingIndex] = newMenu
      } else {
        menus.value.unshift(newMenu)
      }
      return newMenu
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create menu'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateMenu(date: string, dishIds: string[]) {
    loading.value = true
    error.value = null

    try {
      const updatedMenu = await menuService.update(date, dishIds)
      // 更新今日菜单（使用北京时间）
      const today = getTodayBeijing()
      if (today === date) {
        todayMenu.value = updatedMenu
      }
      return updatedMenu
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update menu'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteMenu(date: string) {
    loading.value = true
    error.value = null

    try {
      await menuService.delete(date)
      if (todayMenu.value && todayMenu.value.date === date) {
        todayMenu.value = null
      }
      menus.value = menus.value.filter((m) => m.date !== date)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete menu'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    todayMenu,
    menus,
    loading,
    error,
    hasTodayMenu,
    todayDishes,
    fetchTodayMenu,
    fetchMenus,
    createMenu,
    updateMenu,
    deleteMenu,
  }
})
