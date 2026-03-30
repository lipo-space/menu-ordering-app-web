<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDishStore } from '@/stores/dishStore'
import PixelButton from '@/components/ui/PixelButton.vue'
import PixelCard from '@/components/ui/PixelCard.vue'
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue'
import TrashIcon from '@/components/icons/TrashIcon.vue'
import PaletteIcon from '@/components/icons/PaletteIcon.vue'
import SmileIcon from '@/components/icons/SmileIcon.vue'
import SearchIcon from '@/components/icons/SearchIcon.vue'

const route = useRoute()
const router = useRouter()
const dishStore = useDishStore()

const dishId = computed(() => route.params.id as string)
const dish = computed(() => dishStore.dishes.find(d => d.id === dishId.value))
const loading = ref(false)
const isEditing = ref(false)
const showDeleteDialog = ref(false)
const editForm = ref({
  name: '',
  description: ''
})

onMounted(async () => {
  if (dishStore.dishes.length === 0) {
    loading.value = true
    await dishStore.fetchDishes()
    loading.value = false
  }
})

function goBack() {
  // 检查是否有历史记录
  if (window.history.length > 1) {
    router.back()
  } else {
    // 如果没有历史记录，默认返回首页
    router.push('/')
  }
}

function startEditing() {
  if (dish.value) {
    editForm.value = {
      name: dish.value.name,
      description: dish.value.description || ''
    }
    isEditing.value = true
  }
}

function cancelEditing() {
  isEditing.value = false
  editForm.value = { name: '', description: '' }
}

async function saveEditing() {
  if (!editForm.value.name.trim()) return

  try {
    await dishStore.updateDish(dishId.value, editForm.value)
    isEditing.value = false
  } catch (error) {
    console.error('Failed to update dish:', error)
  }
}

function openDeleteDialog() {
  showDeleteDialog.value = true
}

function closeDeleteDialog() {
  showDeleteDialog.value = false
}

async function confirmDelete() {
  try {
    await dishStore.deleteDish(dishId.value)
    showDeleteDialog.value = false
    // 返回上一页
    router.back()
  } catch (error) {
    console.error('Failed to delete dish:', error)
  }
}
</script>

<template>
  <div class="dish-detail-page">
    <div class="container">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- Dish Details -->
      <div v-else-if="dish" class="dish-detail">
        <!-- Back Button -->
        <div class="back-section">
          <PixelButton variant="secondary" size="sm" @click="goBack">
            ← 返回
          </PixelButton>
        </div>

        <!-- Main Card -->
        <PixelCard class="detail-card">
          <!-- View Mode -->
          <div v-if="!isEditing">
            <div class="dish-header">
              <h1 class="dish-title">{{ dish.name }}</h1>
              <div class="dish-actions">
                <PixelButton variant="primary" size="sm" @click="startEditing">
                  ✏️ 编辑
                </PixelButton>
                <PixelButton variant="danger" size="sm" @click="openDeleteDialog">
                  <trash-icon :size="16" />
                  删除
                </PixelButton>
              </div>
            </div>

            <div v-if="dish.description" class="dish-description">
              <h3 class="section-title">描述</h3>
              <p>{{ dish.description }}</p>
            </div>

            <div class="dish-stats">
              <h3 class="section-title">统计数据</h3>
              <div class="stats-grid">
                <div class="stat-card">
                  <div class="stat-icon">
                    <palette-icon :size="24" />
                  </div>
                  <div class="stat-info">
                    <div class="stat-label">搭配次数</div>
                    <div class="stat-value">{{ dish.times_paired }}</div>
                  </div>
                </div>

                <div class="stat-card">
                  <div class="stat-icon">
                    <smile-icon :size="24" />
                  </div>
                  <div class="stat-info">
                    <div class="stat-label">享用次数</div>
                    <div class="stat-value">{{ dish.times_enjoyed }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="dish-info">
              <h3 class="section-title">菜品信息</h3>
              <div class="info-list">
                <div class="info-item">
                  <span class="info-label">ID:</span>
                  <span class="info-value">{{ dish.id }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Edit Mode -->
          <div v-else class="edit-mode">
            <h2 class="edit-title">✏️ 编辑菜品</h2>

            <form @submit.prevent="saveEditing" class="edit-form">
              <div class="form-group">
                <label class="form-label" for="edit-name">
                  菜品名称 <span class="required">*</span>
                </label>
                <input
                  id="edit-name"
                  v-model="editForm.name"
                  type="text"
                  class="form-input"
                  placeholder="例如：红烧肉"
                  required
                  maxlength="100"
                />
              </div>

              <div class="form-group">
                <label class="form-label" for="edit-description">
                  描述（可选）
                </label>
                <textarea
                  id="edit-description"
                  v-model="editForm.description"
                  class="form-textarea"
                  placeholder="例如：经典家常菜，肥而不腻"
                  rows="3"
                  maxlength="500"
                />
              </div>

              <div class="form-actions">
                <PixelButton type="button" variant="secondary" @click="cancelEditing">
                  取消
                </PixelButton>
                <PixelButton type="submit" variant="primary">
                  保存
                </PixelButton>
              </div>
            </form>
          </div>
        </PixelCard>
      </div>

      <!-- Not Found State -->
      <div v-else class="not-found">
        <PixelCard class="not-found-card">
          <div class="not-found-icon">
            <search-icon :size="80" />
          </div>
          <h2 class="not-found-title">菜品未找到</h2>
          <p class="not-found-text">抱歉，该菜品不存在或已被删除</p>
          <PixelButton variant="primary" @click="goBack">
            返回菜品列表
          </PixelButton>
        </PixelCard>
      </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog
      v-if="showDeleteDialog"
      title="确认删除"
      message="确定要删除这个菜品吗？此操作不可撤销，相关的历史记录也会被移除。"
      confirm-text="删除"
      cancel-text="取消"
      variant="danger"
      @confirm="confirmDelete"
      @cancel="closeDeleteDialog"
    />
  </div>
</template>

<style scoped>
.dish-detail-page {
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

.back-section {
  margin-bottom: 24px;
}

.dish-detail {
  max-width: 800px;
  margin: 0 auto;
}

.detail-card {
  padding: 32px;
}

.dish-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 3px solid #E5E7EB;
}

.dish-title {
  font-size: 2rem;
  color: #1F2937;
  flex: 1;
}

.dish-actions {
  display: flex;
  gap: 12px;
}

.section-title {
  font-size: 1rem;
  color: #1F2937;
  margin-bottom: 16px;
  font-weight: 600;
}

.dish-description {
  margin-bottom: 32px;
}

.dish-description p {
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.6;
}

.dish-stats {
  margin-bottom: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(254, 243, 199, 0.3);
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  transition: all 0.3s;
}

.stat-card:hover {
  background: rgba(254, 243, 199, 0.5);
  border-color: #F59E0B;
  transform: translateY(-2px);
}

.stat-icon {
  width: 40px;
  height: 40px;
  color: #F59E0B;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 0.625rem;
  color: #6B7280;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 1.5rem;
  color: #1F2937;
  font-weight: 600;
}

.dish-info {
  margin-bottom: 24px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  gap: 12px;
  font-size: 0.75rem;
}

.info-label {
  color: #6B7280;
  font-weight: 600;
  min-width: 80px;
}

.info-value {
  color: #1F2937;
}

/* Edit Mode */
.edit-mode {
  animation: fadeIn 0.3s ease-out;
}

.edit-title {
  font-size: 1.5rem;
  margin-bottom: 32px;
  text-align: center;
  color: #1F2937;
}

.edit-form {
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

/* Not Found */
.not-found {
  max-width: 500px;
  margin: 0 auto;
}

.not-found-card {
  text-align: center;
  padding: 60px 40px;
}

.not-found-icon {
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

.not-found-title {
  font-size: 1.25rem;
  margin-bottom: 16px;
  color: #1F2937;
}

.not-found-text {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 32px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .dish-title {
    font-size: 1.5rem;
  }

  .dish-header {
    flex-direction: column;
    gap: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 16px;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
