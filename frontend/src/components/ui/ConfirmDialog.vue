<script setup lang="ts">
defineProps<{
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'warning' | 'info'
}>()

defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <div class="dialog-overlay" @click="$emit('cancel')">
    <div class="dialog-content" @click.stop>
      <div class="dialog-icon">
        {{ variant === 'danger' ? '⚠️' : variant === 'warning' ? '⚡' : 'ℹ️' }}
      </div>
      <h2 class="dialog-title">{{ title }}</h2>
      <p class="dialog-message">{{ message }}</p>
      <div class="dialog-actions">
        <PixelButton
          variant="secondary"
          size="sm"
          @click="$emit('cancel')"
        >
          {{ cancelText || '取消' }}
        </PixelButton>
        <PixelButton
          :variant="variant === 'danger' ? 'danger' : 'primary'"
          size="sm"
          @click="$emit('confirm')"
        >
          {{ confirmText || '确定' }}
        </PixelButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 2000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.dialog-content {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border: 3px solid #1F2937;
  border-radius: 16px;
  padding: 32px;
  max-width: 400px;
  width: 100%;
  box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.15);
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

.dialog-icon {
  text-align: center;
  font-size: 4rem;
  margin-bottom: 16px;
  animation: bounce 0.5s ease-out;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.dialog-title {
  font-size: 1.25rem;
  color: #1F2937;
  margin-bottom: 12px;
  text-align: center;
}

.dialog-message {
  font-size: 0.875rem;
  color: #6B7280;
  margin-bottom: 24px;
  text-align: center;
  line-height: 1.6;
}

.dialog-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
}

@media (max-width: 768px) {
  .dialog-content {
    padding: 24px;
  }

  .dialog-actions {
    flex-direction: column;
  }
}
</style>
