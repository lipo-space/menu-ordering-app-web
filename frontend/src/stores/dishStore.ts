import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { dishService, type Dish, type CreateDishRequest } from '@/services/dishService'

export const useDishStore = defineStore('dishes', () => {
  const dishes = ref<Dish[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const searchQuery = ref('')

  // Computed
  const filteredDishes = computed(() => {
    if (!searchQuery.value) return dishes.value

    const query = searchQuery.value.toLowerCase()
    return dishes.value.filter(
      (dish) =>
        dish.name.toLowerCase().includes(query) ||
        (dish.description && dish.description.toLowerCase().includes(query))
    )
  })

  const dishCount = computed(() => dishes.value.length)

  // Actions
  async function fetchDishes(search?: string) {
    loading.value = true
    error.value = null

    try {
      const response = await dishService.getAll(search)
      dishes.value = response.data
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load dishes'
      console.error('Failed to fetch dishes:', e)
    } finally {
      loading.value = false
    }
  }

  async function createDish(dishData: CreateDishRequest) {
    loading.value = true
    error.value = null

    try {
      const newDish = await dishService.create(dishData)
      dishes.value.push(newDish)
      return newDish
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create dish'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateDish(id: string, dishData: Partial<CreateDishRequest>) {
    loading.value = true
    error.value = null

    try {
      const updatedDish = await dishService.update(id, dishData)
      const index = dishes.value.findIndex((d) => d.id === id)
      if (index !== -1) {
        dishes.value[index] = updatedDish
      }
      return updatedDish
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update dish'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteDish(id: string) {
    loading.value = true
    error.value = null

    try {
      await dishService.delete(id)
      dishes.value = dishes.value.filter((d) => d.id !== id)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete dish'
      throw e
    } finally {
      loading.value = false
    }
  }

  function setSearchQuery(query: string) {
    searchQuery.value = query
  }

  return {
    dishes,
    filteredDishes,
    loading,
    error,
    dishCount,
    searchQuery,
    fetchDishes,
    createDish,
    updateDish,
    deleteDish,
    setSearchQuery,
  }
})
