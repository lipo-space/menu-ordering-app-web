<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useDishStore } from '@/stores/dishStore'
import PixelButton from '@/components/ui/PixelButton.vue'
import PixelCard from '@/components/ui/PixelCard.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import SearchIcon from '@/components/icons/SearchIcon.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import PaletteIcon from '@/components/icons/PaletteIcon.vue'
import SmileIcon from '@/components/icons/SmileIcon.vue'
import PlateIcon from '@/components/icons/PlateIcon.vue'
import type { CreateDishRequest } from '@/services/dishService'

const dishStore = useDishStore()

const showForm = ref(false)
const editingDishId = ref<string | null>(null)
const searchQuery = ref('')
const formData = ref<CreateDishRequest>({
  name: '',
  description: ''
})

const showDeleteDialog = ref(false)
const deleteTargetId = ref<string | null>(null)

onMounted(async () => {
  await dishStore.fetchDishes()
})

const filteredDishes = computed(() => {
  if (!searchQuery.value) return dishStore.dishes

  const query = searchQuery.value.toLowerCase()
  return dishStore.dishes.filter(dish =>
    dish.name.toLowerCase().includes(query) ||
    (dish.description && dish.description.toLowerCase().includes(query))
  )
})

function openCreateForm() {
  editingDishId.value = null
  formData.value = { name: '', description: '' }
  showForm.value = true
}

function openEditForm(dishId: string) {
  const dish = dishStore.dishes.find(d => d.id === dishId)
  if (dish) {
    editingDishId.value = dishId
    formData.value = {
      name: dish.name,
      description: dish.description || ''
    }
    showForm.value = true
  }
}

function closeForm() {
  showForm.value = false
  editingDishId.value = null
  formData.value = { name: '', description: '' }
}

async function handleSubmit() {
  if (!formData.value.name.trim()) return

  try {
    if (editingDishId.value) {
      await dishStore.updateDish(editingDishId.value, formData.value)
    } else {
      await dishStore.createDish(formData.value)
    }
    closeForm()
  } catch (error) {
    console.error('Failed to save dish:', error)
  }
}

function openDeleteConfirm(dishId: string) {
  deleteTargetId.value = dishId
  showDeleteDialog.value = true
}

function closeDeleteConfirm() {
  showDeleteDialog.value = false
  deleteTargetId.value = null
}

async function confirmDelete() {
  if (!deleteTargetId.value) return

  try {
    await dishStore.deleteDish(deleteTargetId.value)
    closeDeleteConfirm()
  } catch (error) {
    console.error('Failed to delete dish:', error)
  }
}

function handleSearch() {
  dishStore.setSearchQuery(searchQuery.value)
}
</script>

<template>
  <div class="dishes-page">
    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <h1 class="page-title">菜品管理</h1>
        <p class="page-subtitle">管理您的家庭菜品库</p>
      </div>

      <!-- Actions Bar -->
      <div class="actions-bar">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索菜品..."
            class="search-input"
            @input="handleSearch"
          />
          <search-icon class="search-icon" :size="20" />
        </div>

        <PixelButton variant="primary" @click="openCreateForm">
          <span class="btn-icon">➕</span>
          添加菜品
        </PixelButton>
      </div>

      <!-- Loading State -->
      <div v-if="dishStore.loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Dishes Grid -->
      <div v-else-if="filteredDishes.length > 0" class="dishes-grid">
        <PixelCard
          v-for="dish in filteredDishes"
          :key="dish.id"
          class="dish-card"
          hoverable
          @click="$router.push(`/dishes/${dish.id}`)"
        >
          <div class="dish-header">
            <h3 class="dish-name">{{ dish.name }}</h3>
            <div class="dish-actions">
              <button
                class="action-btn edit-btn"
                @click.stop="openEditForm(dish.id)"
                title="编辑"
              >
                ✏️
              </button>
              <button
                class="action-btn delete-btn"
                @click.stop="openDeleteConfirm(dish.id)"
                title="删除"
              >
                <trash-icon :size="16" />
              </button>
            </div>
          </div>

          <p v-if="dish.description" class="dish-description">
            {{ dish.description }}
          </p>

          <div class="dish-stats">
            <div class="stat-item">
              <palette-icon class="stat-icon" :size="16" />
              <span class="stat-label">搭配</span>
              <span class="stat-value">{{ dish.times_paired }}</span>
            </div>
            <div class="stat-item">
              <smile-icon class="stat-icon" :size="16" />
              <span class="stat-label">享用</span>
              <span class="stat-value">{{ dish.times_enjoyed }}</span>
            </div>
          </div>
        </PixelCard>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <PixelCard class="empty-card">
          <div class="empty-icon">
            <plate-icon :size="80" />
          </div>
          <h2 class="empty-title">还没有菜品</h2>
          <p class="empty-text">点击上方按钮添加第一个菜品吧！</p>
        </PixelCard>
      </div>

      <!-- Form Modal -->
      <div v-if="showForm" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <PixelCard class="form-card">
            <h2 class="form-title">
              {{ editingDishId ? '✏️ 编辑菜品' : '➕ 添加菜品' }}
            </h2>

            <form @submit.prevent="handleSubmit" class="dish-form">
              <div class="form-group">
                <label class="form-label" for="dish-name">
                  菜品名称 <span class="required">*</span>
                </label>
                <input
                  id="dish-name"
                  v-model="formData.name"
                  type="text"
                  class="form-input"
                  placeholder="例如：红烧肉"
                  required
                  maxlength="100"
                />
              </div>

              <div class="form-group">
                <label class="form-label" for="dish-description">
                  描述（可选）
                </label>
                <textarea
                  id="dish-description"
                  v-model="formData.description"
                  class="form-textarea"
                  placeholder="例如：经典家常菜，肥而不腻"
                  rows="3"
                  maxlength="500"
                />
              </div>

              <div class="form-actions">
                <PixelButton type="button" variant="secondary" @click="closeForm">
                  取消
                </PixelButton>
                <PixelButton type="submit" variant="primary">
                  {{ editingDishId ? '保存' : '添加' }}
                </PixelButton>
              </div>
            </form>
          </PixelCard>
        </div>
      </div>

      <!-- Delete Confirmation Dialog -->
      <ConfirmDialog
        v-if="showDeleteDialog"
        title="确认删除"
        message="确定要删除这个菜品吗？此操作不可撤销。"
        confirm-text="删除"
        cancel-text="取消"
        variant="danger"
        @confirm="confirmDelete"
        @cancel="closeDeleteConfirm"
      />

      <!-- Error State -->
      <div v-if="dishStore.error" class="error-state">
        <p class="error-message">⚠️ {{ dishStore.error }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dishes-page {
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

/* Actions Bar */
.actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 200px;
  max-width: 400px;
  position: relative;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 2px solid #1F2937;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.8);
  font-family: inherit;
  font-size: 0.75rem;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  background: white;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #6B7280;
}

.btn-icon {
  margin-right: 8px;
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

/* Dishes Grid */
.dishes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.dish-card {
  padding: 24px;
}

.dish-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.dish-name {
  font-size: 1rem;
  color: #1F2937;
  flex: 1;
  margin-right: 12px;
}

.dish-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid #D1D5DB;
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.action-btn:hover {
  transform: scale(1.1);
}

.edit-btn:hover {
  background: #DBEAFE;
  border-color: #3B82F6;
}

.delete-btn:hover {
  background: #FEE2E2;
  border-color: #EF4444;
}

.dish-description {
  font-size: 0.625rem;
  color: #6B7280;
  line-height: 1.6;
  margin-bottom: 16px;
}

.dish-stats {
  display: flex;
  gap: 16px;
  padding-top: 16px;
  border-top: 2px dashed #D1D5DB;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.625rem;
}

.stat-icon {
  width: 16px;
  height: 16px;
  color: #F59E0B;
  flex-shrink: 0;
}

.stat-label {
  color: #6B7280;
}

.stat-value {
  color: #1F2937;
  font-weight: 600;
}

/* Empty State */
.empty-card {
  text-align: center;
  padding: 60px 40px;
  max-width: 500px;
  margin: 0 auto;
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
  line-height: 1.6;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-card {
  padding: 32px;
}

.form-title {
  font-size: 1.25rem;
  margin-bottom: 24px;
  text-align: center;
}

.dish-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
}

.required {
  color: #EF4444;
}

.form-input,
.form-textarea {
  padding: 12px 16px;
  border: 2px solid #D1D5DB;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.875rem;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.8);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #F59E0B;
  background: white;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 8px;
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
  font-size: 0.75rem;
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.5rem;
  }

  .actions-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: none;
  }

  .dishes-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
