<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDishStore } from '@/stores/dishStore'
import { useMenuStore } from '@/stores/menuStore'
import { useCombinationStore } from '@/stores/combinationStore'
import PixelButton from '@/components/ui/PixelButton.vue'
import PixelCard from '@/components/ui/PixelCard.vue'
import HomeIcon from '@/components/icons/HomeIcon.vue'
import PlateIcon from '@/components/icons/PlateIcon.vue'
import SaladIcon from '@/components/icons/SaladIcon.vue'
import PaletteIcon from '@/components/icons/PaletteIcon.vue'
import NoteIcon from '@/components/icons/NoteIcon.vue'
import { getTodayBeijing } from '@/utils/dateUtils'

const router = useRouter()
const route = useRoute()
const dishStore = useDishStore()
const menuStore = useMenuStore()
const combinationStore = useCombinationStore()

const showMenuCreation = ref(false)
const selectedDishIds = ref<string[]>([])
const selectionMode = ref<'dishes' | 'combinations'>('dishes')

onMounted(async () => {
  await Promise.all([
    dishStore.fetchDishes(),
    menuStore.fetchTodayMenu(),
    combinationStore.fetchCombinations()
  ])

  // 检查 URL 参数，如果是编辑模式则自动打开
  const { edit, dishes } = route.query
  if (edit === 'true' && dishes) {
    const dishIds = (dishes as string).split(',').filter(id => id)
    if (dishIds.length > 0) {
      selectedDishIds.value = dishIds
      showMenuCreation.value = true
    }
  }
})

const todayDate = computed(() => {
  const today = new Date()
  return today.toLocaleDateString('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})

function toggleDishSelection(dishId: string) {
  const index = selectedDishIds.value.indexOf(dishId)
  if (index > -1) {
    selectedDishIds.value.splice(index, 1)
  } else {
    selectedDishIds.value.push(dishId)
  }
}

function useCombination(combination: any) {
  // 清空当前选择，添加搭配中的所有菜品
  selectedDishIds.value = combination.dishes.map((d: any) => d.id)
}

async function saveMenu() {
  if (selectedDishIds.value.length === 0) return

  try {
    const today = getTodayBeijing()
    await menuStore.createMenu(today, selectedDishIds.value)
    showMenuCreation.value = false
    selectedDishIds.value = []
  } catch (error) {
    console.error('Failed to save menu:', error)
  }
}

function startCreatingMenu() {
  showMenuCreation.value = true
  selectedDishIds.value = menuStore.todayDishes.map(d => d.id) || []
}

function cancelCreation() {
  showMenuCreation.value = false
  selectedDishIds.value = []
}

function goToDishDetail(dishId: string) {
  router.push(`/dishes/${dishId}`)
}
</script>

<template>
  <div class="home-page">
    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <h1 class="page-title">
          <home-icon class="title-icon" :size="40" />
          今日菜单
        </h1>
        <p class="page-date">{{ todayDate }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="menuStore.loading || dishStore.loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Menu Display -->
      <div v-else-if="menuStore.hasTodayMenu && !showMenuCreation" class="menu-display">
        <PixelCard class="today-menu-card">
          <h2 class="menu-title">今日菜肴</h2>
          <div class="dishes-grid">
            <div
              v-for="dish in menuStore.todayDishes"
              :key="dish.id"
              class="dish-item"
              @click="goToDishDetail(dish.id)"
            >
              <div class="dish-icon">
                <plate-icon :size="40" />
              </div>
              <div class="dish-info">
                <h3 class="dish-name">{{ dish.name }}</h3>
                <p v-if="dish.description" class="dish-description">
                  {{ dish.description }}
                </p>
                <div class="dish-stats">
                  <salad-icon class="stat-icon" :size="16" />
                  <span class="stat-text">已享用 {{ dish.times_enjoyed }} 次</span>
                </div>
              </div>
            </div>
          </div>
          <div class="menu-actions">
            <PixelButton variant="secondary" @click="startCreatingMenu">
              编辑菜单
            </PixelButton>
          </div>
        </PixelCard>
      </div>

      <!-- Menu Creation -->
      <div v-else-if="showMenuCreation" class="menu-creation">
        <PixelCard class="creation-card">
          <h2 class="creation-title">选择今日菜肴</h2>

          <!-- Mode Tabs -->
          <div class="mode-tabs">
            <button
              class="mode-tab"
              :class="{ 'mode-tab--active': selectionMode === 'dishes' }"
              @click="selectionMode = 'dishes'"
            >
              <plate-icon :size="20" />
              <span class="tab-text">选择菜品</span>
            </button>
            <button
              class="mode-tab"
              :class="{ 'mode-tab--active': selectionMode === 'combinations' }"
              @click="selectionMode = 'combinations'"
            >
              <palette-icon :size="20" />
              <span class="tab-text">选择搭配</span>
            </button>
          </div>

          <!-- Selected Dishes -->
          <div v-if="selectedDishIds.length > 0" class="selected-section">
            <h3>已选 ({{ selectedDishIds.length }})</h3>
            <div class="selected-dishes">
              <div
                v-for="dishId in selectedDishIds"
                :key="dishId"
                class="selected-dish-chip"
                @click="toggleDishSelection(dishId)"
              >
                {{ dishStore.dishes.find(d => d.id === dishId)?.name }}
                <span class="remove-icon">×</span>
              </div>
            </div>
          </div>

          <!-- Dishes Selection Mode -->
          <div v-if="selectionMode === 'dishes'" class="dishes-selection">
            <h3>可选菜品</h3>
            <div class="dishes-grid">
              <div
                v-for="dish in dishStore.dishes"
                :key="dish.id"
                class="dish-option"
                :class="{ 'dish-option--selected': selectedDishIds.includes(dish.id) }"
                @click="toggleDishSelection(dish.id)"
              >
                <div class="dish-header">
                  <span class="dish-name">{{ dish.name }}</span>
                  <span v-if="selectedDishIds.includes(dish.id)" class="check-icon">✓</span>
                </div>
                <p v-if="dish.description" class="dish-desc">{{ dish.description }}</p>
              </div>
            </div>
          </div>

          <!-- Combinations Selection Mode -->
          <div v-else class="combinations-selection">
            <h3>可用搭配</h3>
            <div v-if="combinationStore.combinations.length > 0" class="combinations-list">
              <div
                v-for="combination in combinationStore.combinations"
                :key="combination.id"
                class="combination-option"
                @click="useCombination(combination)"
              >
                <div class="combination-header">
                  <h4 class="combination-name">{{ combination.name }}</h4>
                  <span class="dish-count">{{ combination.dishes.length }} 道菜</span>
                </div>
                <div class="combination-dishes">
                  <span
                    v-for="dish in combination.dishes"
                    :key="dish.id"
                    class="dish-tag"
                  >
                    {{ dish.name }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="no-combinations">
              <p>还没有保存的搭配</p>
              <router-link to="/combinations">
                <PixelButton variant="secondary" size="sm">
                  去创建搭配
                </PixelButton>
              </router-link>
            </div>
          </div>

          <!-- Actions -->
          <div class="creation-actions">
            <PixelButton variant="secondary" @click="cancelCreation">
              取消
            </PixelButton>
            <PixelButton
              variant="primary"
              :disabled="selectedDishIds.length === 0"
              @click="saveMenu"
            >
              保存菜单
            </PixelButton>
          </div>
        </PixelCard>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <PixelCard class="empty-card">
          <div class="empty-icon">
            <note-icon :size="80" />
          </div>
          <h2 class="empty-title">今天还没有菜单</h2>
          <p class="empty-text">点击下方按钮开始创建今日菜单吧！</p>
          <PixelButton variant="primary" size="lg" @click="startCreatingMenu">
            创建今日菜单
          </PixelButton>
        </PixelCard>
      </div>

      <!-- Error State -->
      <div v-if="menuStore.error || dishStore.error" class="error-state">
        <p class="error-message">
          ⚠️ {{ menuStore.error || dishStore.error }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  padding: 32px 0;
  min-height: calc(100vh - 120px);
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  color: #1F2937;
  margin-bottom: 12px;
  animation: bounce 1s ease-out;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.title-icon {
  color: #F59E0B;
  animation: bounce 1s ease-out;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.page-date {
  font-size: 0.875rem;
  color: #6B7280;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #FDE68A;
  border-top-color: #F59E0B;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Cards */
.today-menu-card,
.creation-card,
.empty-card {
  max-width: 900px;
  margin: 0 auto;
}

.menu-title,
.creation-title {
  font-size: 1.5rem;
  margin-bottom: 24px;
  color: #1F2937;
}

/* Dishes Grid */
.dishes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.dish-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid #1F2937;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.dish-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 1);
}

.dish-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  color: #F59E0B;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dish-info {
  flex: 1;
}

.dish-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 8px;
}

.dish-description {
  font-size: 0.75rem;
  color: #6B7280;
  line-height: 1.5;
  margin-bottom: 12px;
}

.dish-stats {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.625rem;
  color: #6B7280;
}

.stat-icon {
  color: #F59E0B;
  flex-shrink: 0;
}

.stat-text {
  line-height: 1;
}

/* Mode Tabs */
.mode-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 2px solid #E5E7EB;
  padding-bottom: 12px;
}

.mode-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.5);
  border: 2px solid #D1D5DB;
  border-radius: 12px 12px 0 0;
  cursor: pointer;
  transition: all 0.3s;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
}

.mode-tab:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: #F59E0B;
}

.mode-tab--active {
  background: #FEF3C7;
  border-color: #F59E0B;
  color: #1F2937;
  border-bottom: 2px solid #FEF3C7;
  margin-bottom: -14px;
}

/* Selected Section */
.selected-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px dashed #D1D5DB;
}

.selected-section h3 {
  font-size: 0.875rem;
  margin-bottom: 16px;
  color: #374151;
}

.selected-dishes {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.selected-dish-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #F59E0B;
  color: #1F2937;
  border: 2px solid #1F2937;
  border-radius: 20px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.selected-dish-chip:hover {
  background: #FBBF24;
  transform: scale(1.05);
}

.remove-icon {
  font-size: 1rem;
  font-weight: bold;
}

/* Dishes Selection */
.dishes-selection h3 {
  font-size: 0.875rem;
  margin-bottom: 16px;
  color: #374151;
}

.dish-option {
  padding: 16px;
  background: rgba(255, 255, 255, 0.5);
  border: 2px solid #D1D5DB;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dish-option:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: #F59E0B;
  transform: translateY(-2px);
}

.dish-option--selected {
  background: #FEF3C7;
  border-color: #F59E0B;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.dish-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.dish-option .dish-name {
  font-size: 0.875rem;
  margin-bottom: 0;
}

.check-icon {
  color: #059669;
  font-size: 1.25rem;
  font-weight: bold;
}

.dish-desc {
  font-size: 0.625rem;
  color: #6B7280;
  line-height: 1.4;
}

/* Combinations Selection */
.combinations-selection h3 {
  font-size: 0.875rem;
  margin-bottom: 16px;
  color: #374151;
}

.combinations-list {
  display: grid;
  gap: 16px;
}

.combination-option {
  padding: 20px;
  background: rgba(255, 255, 255, 0.5);
  border: 2px solid #D1D5DB;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.combination-option:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: #F59E0B;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
}

.combination-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.combination-name {
  font-size: 1rem;
  color: #1F2937;
  font-weight: 600;
}

.dish-count {
  font-size: 0.75rem;
  color: #6B7280;
  background: #FEF3C7;
  padding: 4px 12px;
  border-radius: 12px;
  border: 2px solid #F59E0B;
}

.combination-dishes {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dish-tag {
  padding: 6px 12px;
  background: #FEF3C7;
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  font-size: 0.625rem;
  color: #1F2937;
}

.no-combinations {
  text-align: center;
  padding: 40px 20px;
  color: #6B7280;
}

.no-combinations p {
  margin-bottom: 16px;
  font-size: 0.875rem;
}

/* Actions */
.menu-actions,
.creation-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
}

/* Empty State */
.empty-card {
  text-align: center;
  padding: 60px 40px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  color: #D1D5DB;
  animation: bounce 2s infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-title {
  font-size: 1.25rem;
  margin-bottom: 16px;
  color: #1F2937;
}

.empty-text {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 32px;
  line-height: 1.6;
}

/* Error State */
.error-state {
  margin-top: 24px;
  text-align: center;
}

.error-message {
  color: #DC2626;
  background: #FEE2E2;
  padding: 16px;
  border-radius: 8px;
  border: 2px solid #DC2626;
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.75rem;
  }

  .dishes-grid {
    grid-template-columns: 1fr;
  }

  .mode-tabs {
    flex-direction: column;
  }

  .mode-tab--active {
    margin-bottom: 0;
  }

  .creation-actions {
    flex-direction: column;
  }
}
</style>
