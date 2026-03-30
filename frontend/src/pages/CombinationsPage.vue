<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCombinationStore } from '@/stores/combinationStore'
import { useDishStore } from '@/stores/dishStore'
import PixelButton from '@/components/ui/PixelButton.vue'
import PixelCard from '@/components/ui/PixelCard.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import AddIcon from '@/components/icons/AddIcon.vue'
import editIcon from '@/components/icons/EditIcon.vue'
import deleteIcon from '@/components/icons/DeleteIcon.vue'
import searchIcon from '@/components/icons/SearchIcon.vue'

const router = useRouter()
const combinationStore = useCombinationStore()
const dishStore = useDishStore()

const showForm = ref(false)
const editingCombinationId = ref<string | null>(null)
const searchQuery = ref('')
const formData = ref({
  name: '',
  dish_ids: [] as string[]
})

const showDeleteDialog = ref(false)
const deleteTargetId = ref<string | null>(null)

onMounted(async () => {
  await Promise.all([
    combinationStore.fetchCombinations(),
    dishStore.fetchDishes()
  ])
})

const filteredCombinations = computed(() => {
  if (!searchQuery.value) return combinationStore.combinations

  const query = searchQuery.value.toLowerCase()
  return combinationStore.combinations.filter(combination =>
    combination.name.toLowerCase().includes(query)
  )
})

function openCreateForm() {
  editingCombinationId.value = null
  formData.value = { name: '', dish_ids: [] }
  showForm.value = true
}

function openEditForm(combinationId: string) {
  const combination = combinationStore.combinations.find(c => c.id === combinationId)
  if (combination) {
    editingCombinationId.value = combinationId
    formData.value = {
      name: combination.name,
      dish_ids: combination.dishes.map((d: any) => d.id)
    }
    showForm.value = true
  }
}

function closeForm() {
  showForm.value = false
  editingCombinationId.value = null
  formData.value = { name: '', dish_ids: [] }
}

function toggleDish(dishId: string) {
  const index = formData.value.dish_ids.indexOf(dishId)
  if (index > -1) {
    formData.value.dish_ids.splice(index, 1)
  } else {
    formData.value.dish_ids.push(dishId)
  }
}

async function handleSubmit() {
  if (!formData.value.name.trim() || formData.value.dish_ids.length === 0) return

  try {
    if (editingCombinationId.value) {
      await combinationStore.updateCombination(editingCombinationId.value, {
        name: formData.value.name,
        dish_ids: formData.value.dish_ids
      })
    } else {
      await combinationStore.createCombination({
        name: formData.value.name,
        dish_ids: formData.value.dish_ids
      })
    }
    closeForm()
  } catch (error) {
    console.error('Failed to save combination:', error)
  }
}

function openDeleteConfirm(combinationId: string) {
  deleteTargetId.value = combinationId
  showDeleteDialog.value = true
}

function closeDeleteConfirm() {
  showDeleteDialog.value = false
  deleteTargetId.value = null
}

async function confirmDelete() {
  if (!deleteTargetId.value) return

  try {
    await combinationStore.deleteCombination(deleteTargetId.value)
    closeDeleteConfirm()
  } catch (error) {
    console.error('Failed to delete combination:', error)
  }
}

function useCombination(combination: any) {
  // 跳转到首页并打开编辑模式，自动选择该搭配的菜品
  const dishIds = combination.dishes.map((d: any) => d.id).join(',')
  router.push(`/?edit=true&dishes=${dishIds}`)
}
</script>

<template>
  <div class="combinations-page">
    <div class="container">
      <!-- Header -->
      <div class="page-header">
        <h1 class="page-title">搭配清单</h1>
        <p class="page-subtitle">快速创建常用菜品搭配</p>
      </div>

      <!-- Actions Bar -->
      <div class="actions-bar">
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索搭配..."
            class="search-input"
          />
          <search-icon class="search-icon" :size="20" />
        </div>

        <PixelButton variant="primary" @click="openCreateForm">
          <add-icon :size="16" />
          <span class="btn-text">创建搭配</span>
        </PixelButton>
      </div>

      <!-- Loading State -->
      <div v-if="combinationStore.loading || dishStore.loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Combinations Grid -->
      <div v-else-if="filteredCombinations.length > 0" class="combinations-grid">
        <PixelCard
          v-for="combination in filteredCombinations"
          :key="combination.id"
          class="combination-card"
          hoverable
        >
          <div class="combination-header">
            <h3 class="combination-name">{{ combination.name }}</h3>
            <div class="combination-actions">
              <button
                class="action-btn edit-btn"
                @click.stop="openEditForm(combination.id)"
                title="编辑"
              >
                <edit-icon :size="16" />
              </button>
              <button
                class="action-btn delete-btn"
                @click.stop="openDeleteConfirm(combination.id)"
                title="删除"
              >
                <delete-icon :size="16" />
              </button>
            </div>
          </div>

          <div class="combination-dishes">
            <div
              v-for="dish in combination.dishes"
              :key="dish.id"
              class="dish-chip"
            >
              {{ dish.name }}
            </div>
          </div>

          <div class="combination-footer">
            <div class="combination-meta">
              <span class="meta-item">
                <span class="meta-label">菜品数量:</span>
                <span class="meta-value">{{ combination.dishes.length }}</span>
              </span>
            </div>
            <PixelButton
              variant="primary"
              size="sm"
              @click="useCombination(combination)"
            >
              使用此搭配
            </PixelButton>
          </div>
        </PixelCard>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <PixelCard class="empty-card">
          <div class="empty-icon">
            <search-icon :size="80" />
          </div>
          <h2 class="empty-title">还没有搭配</h2>
          <p class="empty-text">创建您的第一个菜品搭配吧！</p>
          <PixelButton variant="primary" @click="openCreateForm">
            创建搭配
          </PixelButton>
        </PixelCard>
      </div>

      <!-- Form Modal -->
      <div v-if="showForm" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <PixelCard class="form-card">
            <h2 class="form-title">
              {{ editingCombinationId ? '编辑搭配' : '创建搭配' }}
            </h2>

            <form @submit.prevent="handleSubmit" class="combination-form">
              <div class="form-group">
                <label class="form-label" for="combination-name">
                  搭配名称 <span class="required">*</span>
                </label>
                <input
                  id="combination-name"
                  v-model="formData.name"
                  type="text"
                  class="form-input"
                  placeholder="例如：周末家常菜"
                  required
                  maxlength="100"
                />
              </div>

              <div class="form-group">
                <label class="form-label">
                  选择菜品 <span class="required">*</span>
                </label>
                <div class="dishes-selection">
                  <div
                    v-for="dish in dishStore.dishes"
                    :key="dish.id"
                    class="dish-option"
                    :class="{ 'dish-option--selected': formData.dish_ids.includes(dish.id) }"
                    @click="toggleDish(dish.id)"
                  >
                    <div class="dish-option-header">
                      <span class="dish-option-name">{{ dish.name }}</span>
                      <span v-if="formData.dish_ids.includes(dish.id)" class="check-mark">✓</span>
                    </div>
                    <p v-if="dish.description" class="dish-option-desc">
                      {{ dish.description }}
                    </p>
                  </div>
                </div>
              </div>

              <div class="form-actions">
                <PixelButton type="button" variant="secondary" @click="closeForm">
                  取消
                </PixelButton>
                <PixelButton
                  type="submit"
                  variant="primary"
                  :disabled="!formData.name.trim() || formData.dish_ids.length === 0"
                >
                  {{ editingCombinationId ? '保存' : '创建' }}
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
        message="确定要删除这个搭配吗？此操作不可撤销。"
        confirm-text="删除"
        cancel-text="取消"
        variant="danger"
        @confirm="confirmDelete"
        @cancel="closeDeleteConfirm"
      />

      <!-- Error State -->
      <div v-if="combinationStore.error" class="error-state">
        <p class="error-message">⚠️ {{ combinationStore.error }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.combinations-page {
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
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 2px solid #D1D5DB;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  font-family: inherit;
  font-size: 0.875rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-input:focus {
  outline: none;
  border-color: #F59E0B;
  background: white;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
}

.search-icon {
  position: absolute;
  left: 16px;
  color: #6B7280;
}

.btn-text {
  margin-left: 8px;
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

/* Combinations Grid */
.combinations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.combination-card {
  padding: 24px;
}

.combination-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.combination-name {
  font-size: 1.125rem;
  color: #1F2937;
  flex: 1;
}

.combination-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid #E5E7EB;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.edit-btn:hover {
  background: #DBEAFE;
  border-color: #3B82F6;
  color: #3B82F6;
}

.delete-btn:hover {
  background: #FEE2E2;
  border-color: #EF4444;
  color: #EF4444;
}

.combination-dishes {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
}

.dish-chip {
  padding: 8px 16px;
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border: 2px solid #1F2937;
  border-radius: 20px;
  font-size: 0.875rem;
  color: #1F2937;
  transition: all 0.2s;
}

.dish-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.combination-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 2px dashed #E5E7EB;
}

.combination-meta {
  display: flex;
  gap: 16px;
}

.meta-item {
  font-size: 0.75rem;
  color: #6B7280;
}

.meta-label {
  margin-right: 4px;
}

.meta-value {
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
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.form-card {
  padding: 32px;
}

.form-title {
  font-size: 1.5rem;
  margin-bottom: 24px;
  text-align: center;
  color: #1F2937;
}

.combination-form {
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
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.required {
  color: #EF4444;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #D1D5DB;
  border-radius: 12px;
  font-family: inherit;
  font-size: 0.875rem;
  transition: all 0.3s;
  background: rgba(255, 255, 255, 0.9);
}

.form-input:focus {
  outline: none;
  border-color: #F59E0B;
  background: white;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
}

.dishes-selection {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;
  padding: 8px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
}

.dish-option {
  padding: 16px;
  background: rgba(255, 255, 255, 0.5);
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dish-option:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: #F59E0B;
  transform: translateY(-2px);
}

.dish-option--selected {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border-color: #F59E0B;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
}

.dish-option-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.dish-option-name {
  font-size: 0.875rem;
  color: #1F2937;
  font-weight: 600;
}

.check-mark {
  color: #10B981;
  font-size: 1.25rem;
  font-weight: bold;
}

.dish-option-desc {
  font-size: 0.75rem;
  color: #6B7280;
  line-height: 1.4;
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
  font-size: 0.875rem;
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

  .combinations-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .combination-footer {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
