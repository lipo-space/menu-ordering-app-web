<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMenuStore } from '@/stores/menuStore'
import PixelCard from '@/components/ui/PixelCard.vue'
import PixelButton from '@/components/ui/PixelButton.vue'
import CalendarIcon from '@/components/icons/CalendarIcon.vue'
import FilterIcon from '@/components/icons/FilterIcon.vue'
import DishIcon from '@/components/icons/DishIcon.vue'
import {
  getTodayBeijing,
  getDaysAgoBeijing,
  formatDateBeijing,
  isTodayBeijing
} from '@/utils/dateUtils'

const menuStore = useMenuStore()

const selectedDateRange = ref<'today' | 'week' | 'month' | 'custom' | ''>('')
const customStartDate = ref<string>('')
const customEndDate = ref<string>('')
const showCustomPicker = ref(false)

// Computed filtered menus
const filteredMenus = computed(() => {
  let menus = [...menuStore.menus].sort((a, b) =>
    new Date(b.date).getTime() - new Date(a.date).getTime()
  )

  if (!selectedDateRange.value) return menus

  const today = getTodayBeijing()
  const weekAgo = getDaysAgoBeijing(7)
  const monthAgo = getDaysAgoBeijing(30)

  switch (selectedDateRange.value) {
    case 'today':
      return menus.filter(menu => menu.date === today)
    case 'week':
      return menus.filter(menu => menu.date >= weekAgo)
    case 'month':
      return menus.filter(menu => menu.date >= monthAgo)
    case 'custom':
      if (!customStartDate.value || !customEndDate.value) return menus
      return menus.filter(menu =>
        menu.date >= customStartDate.value && menu.date <= customEndDate.value
      )
    default:
      return menus
  }
})

onMounted(async () => {
  await menuStore.fetchMenus()
})

function setDateRange(range: 'today' | 'week' | 'month' | 'custom') {
  selectedDateRange.value = range
  if (range === 'custom') {
    showCustomPicker.value = true
  } else {
    showCustomPicker.value = false
  }
}

function clearFilter() {
  selectedDateRange.value = ''
  customStartDate.value = ''
  customEndDate.value = ''
  showCustomPicker.value = false
}

function applyCustomFilter() {
  if (customStartDate.value && customEndDate.value) {
    selectedDateRange.value = 'custom'
    showCustomPicker.value = false
  }
}
</script>

<template>
  <div class="history-page">
    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <h1 class="page-title">历史记录</h1>
        <p class="page-subtitle">回顾过去的点菜记录</p>
      </div>

      <!-- Date Filter -->
      <div class="filter-section">
        <div class="filter-container">
          <div class="filter-header">
            <filter-icon :size="20" />
            <span class="filter-title">日期筛选</span>
          </div>

          <div class="quick-filters">
            <button
              v-for="range in (['today', 'week', 'month', 'custom'] as const)"
              :key="range"
              class="quick-filter-btn"
              :class="{ 'quick-filter-btn--active': selectedDateRange === range }"
              @click="setDateRange(range)"
            >
              <span v-if="range === 'today'">今天</span>
              <span v-else-if="range === 'week'">最近一周</span>
              <span v-else-if="range === 'month'">最近一月</span>
              <span v-else>自定义</span>
            </button>
          </div>

          <transition name="slide-fade">
            <div v-if="showCustomPicker" class="custom-picker">
              <div class="date-input-group">
                <label class="date-label">开始日期</label>
                <input
                  v-model="customStartDate"
                  type="date"
                  class="date-input"
                  :max="customEndDate || new Date().toISOString().split('T')[0]"
                />
              </div>

              <div class="date-input-group">
                <label class="date-label">结束日期</label>
                <input
                  v-model="customEndDate"
                  type="date"
                  class="date-input"
                  :min="customStartDate || new Date().toISOString().split('T')[0]"
                />
              </div>

              <PixelButton
                variant="primary"
                size="sm"
                :disabled="!customStartDate || !customEndDate"
                @click="applyCustomFilter"
              >
                应用
              </PixelButton>
            </div>
          </transition>
        </div>

        <PixelButton
          v-if="selectedDateRange"
          variant="secondary"
          size="sm"
          @click="clearFilter"
        >
          清除筛选
        </PixelButton>
      </div>

      <!-- Loading State -->
      <div v-if="menuStore.loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Menus List -->
      <div v-else-if="filteredMenus.length > 0" class="menus-list">
        <PixelCard
          v-for="menu in filteredMenus"
          :key="menu.id"
          class="menu-card"
          hoverable
        >
          <div class="menu-header">
            <div class="menu-date-section">
              <h3 class="menu-date">{{ formatDateBeijing(menu.date) }}</h3>
              <span v-if="isTodayBeijing(menu.date)" class="today-badge">
                今天
              </span>
            </div>
          </div>

          <div class="dishes-grid">
            <div
              v-for="dish in menu.dishes"
              :key="dish.id"
              class="dish-item"
            >
              <div class="dish-icon">
                <dish-icon :size="32" />
              </div>
              <div class="dish-info">
                <h4 class="dish-name">{{ dish.name }}</h4>
                <p v-if="dish.description" class="dish-description">
                  {{ dish.description }}
                </p>
              </div>
            </div>
          </div>

          <div class="menu-footer">
            <div class="menu-meta">
              <span class="meta-item">
                <dish-icon class="meta-icon" :size="16" />
                {{ menu.dishes.length }} 道菜
              </span>
            </div>
          </div>
        </PixelCard>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <PixelCard class="empty-card">
          <div class="empty-icon">
            <calendar-icon :size="80" />
          </div>
          <h2 class="empty-title">
            {{ selectedDateRange ? '该日期范围没有菜单' : '还没有历史记录' }}
          </h2>
          <p class="empty-text">
            {{ selectedDateRange ? '请选择其他日期范围试试' : '创建您的第一个菜单后，历史记录会显示在这里' }}
          </p>
          <PixelButton v-if="selectedDateRange" variant="primary" @click="clearFilter">
            查看所有记录
          </PixelButton>
        </PixelCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-page {
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
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  color: #1F2937;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 0.75rem;
  color: #6B7280;
}

/* Filter Section */
.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-container {
  flex: 1;
  min-width: 280px;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-container:hover {
  border-color: #F59E0B;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.1);
}

.filter-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  color: #374151;
  font-weight: 600;
  font-size: 0.875rem;
}

.filter-title {
  color: #1F2937;
}

.quick-filters {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.quick-filter-btn {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid #D1D5DB;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.75rem;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
}

.quick-filter-btn:hover {
  background: rgba(255, 255, 255, 1);
  border-color: #F59E0B;
  color: #1F2937;
  transform: translateY(-2px);
}

.quick-filter-btn--active {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border-color: #F59E0B;
  color: #1F2937;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
}

.custom-picker {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 2px dashed #E5E7EB;
  display: flex;
  gap: 16px;
  align-items: flex-end;
  flex-wrap: wrap;
  animation: slideFadeIn 0.3s ease-out;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.date-input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 140px;
}

.date-label {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 600;
}

.date-input {
  padding: 10px 14px;
  border: 2px solid #D1D5DB;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.875rem;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.8);
}

.date-input:focus {
  outline: none;
  border-color: #F59E0B;
  background: white;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
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

/* Menus List */
.menus-list {
  display: grid;
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.menu-card {
  padding: 28px;
}

.menu-header {
  margin-bottom: 24px;
}

.menu-date-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-date {
  font-size: 1.125rem;
  color: #1F2937;
}

.today-badge {
  padding: 4px 12px;
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  color: #1F2937;
  border: 2px solid #1F2937;
  border-radius: 12px;
  font-size: 0.625rem;
  font-weight: 600;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Dishes Grid */
.dishes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.dish-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dish-item:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: #F59E0B;
  transform: translateX(4px);
}

.dish-icon {
  width: 32px;
  height: 32px;
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
  font-size: 0.875rem;
  color: #1F2937;
  margin-bottom: 4px;
}

.dish-description {
  font-size: 0.625rem;
  color: #6B7280;
  line-height: 1.4;
}

/* Menu Footer */
.menu-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 2px dashed #D1D5DB;
}

.menu-meta {
  display: flex;
  gap: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.625rem;
  color: #6B7280;
}

.meta-icon {
  width: 16px;
  height: 16px;
  color: #F59E0B;
}

/* Empty State */
.empty-card {
  text-align: center;
  padding: 60px 40px;
  max-width: 500px;
  margin: 0 auto;
}

.empty-icon {
  margin-bottom: 24px;
  color: #D1D5DB;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
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

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }

  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-container {
    max-width: none;
  }

  .quick-filters {
    flex-direction: column;
  }

  .quick-filter-btn {
    width: 100%;
  }

  .custom-picker {
    flex-direction: column;
    align-items: stretch;
  }

  .date-input-group {
    min-width: auto;
  }

  .dishes-grid {
    grid-template-columns: 1fr;
  }

  .menu-meta {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
