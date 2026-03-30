import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { combinationService, type Combination } from '@/services/combinationService'
import { useDishStore } from './dishStore'

export const useCombinationStore = defineStore('combinations', () => {
  const combinations = ref<Combination[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const combinationCount = computed(() => combinations.value.length)

  // Actions
  async function fetchCombinations() {
    loading.value = true
    error.value = null

    try {
      combinations.value = await combinationService.getAll()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load combinations'
      console.error('Failed to fetch combinations:', e)
    } finally {
      loading.value = false
    }
  }

  async function createCombination(data: { name: string; dish_ids: string[] }) {
    loading.value = true
    error.value = null

    try {
      const newCombination = await combinationService.create(data)
      combinations.value.unshift(newCombination)

      // Refresh dishes to update times_paired
      const dishStore = useDishStore()
      await dishStore.fetchDishes()

      return newCombination
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to create combination'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateCombination(id: string, data: { name: string; dish_ids: string[] }) {
    loading.value = true
    error.value = null

    try {
      const updatedCombination = await combinationService.update(id, data)
      const index = combinations.value.findIndex(c => c.id === id)
      if (index !== -1) {
        combinations.value[index] = updatedCombination
      }

      // Refresh dishes to update times_paired
      const dishStore = useDishStore()
      await dishStore.fetchDishes()

      return updatedCombination
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to update combination'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteCombination(id: string) {
    loading.value = true
    error.value = null

    try {
      await combinationService.delete(id)
      combinations.value = combinations.value.filter(c => c.id !== id)

      // Refresh dishes to update times_paired
      const dishStore = useDishStore()
      await dishStore.fetchDishes()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to delete combination'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    combinations,
    loading,
    error,
    combinationCount,
    fetchCombinations,
    createCombination,
    updateCombination,
    deleteCombination
  }
})
