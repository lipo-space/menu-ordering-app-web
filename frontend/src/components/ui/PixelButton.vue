<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
  size?: 'sm' | 'md' | 'lg'
  type?: 'button' | 'submit' | 'reset'
}>()

defineEmits<{
  click: []
}>()
</script>

<template>
  <button
    class="pixel-button"
    :class="[
      `pixel-button--${variant || 'primary'}`,
      `pixel-button--${size || 'md'}`,
      { 'pixel-button--disabled': disabled }
    ]"
    :type="type || 'button'"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<style scoped>
.pixel-button {
  border: 3px solid #1F2937;
  font-family: 'Press Start 2P', monospace;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
  box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.pixel-button:active:not(.pixel-button--disabled) {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.1);
}

/* Variants */
.pixel-button--primary {
  background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
  color: #1F2937;
}

.pixel-button--primary:hover:not(.pixel-button--disabled) {
  background: linear-gradient(135deg, #FCD34D 0%, #FBBF24 100%);
  transform: translateY(-2px);
  box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.15);
}

.pixel-button--secondary {
  background: rgba(255, 255, 255, 0.9);
  color: #1F2937;
}

.pixel-button--secondary:hover:not(.pixel-button--disabled) {
  background: #F3F4F6;
  transform: translateY(-2px);
  box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.15);
}

.pixel-button--danger {
  background: linear-gradient(135deg, #FCA5A5 0%, #F87171 100%);
  color: #1F2937;
}

.pixel-button--danger:hover:not(.pixel-button--disabled) {
  background: linear-gradient(135deg, #FECACA 0%, #FCA5A5 100%);
  transform: translateY(-2px);
  box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.15);
}

/* Focus Visible */
.pixel-button:focus-visible {
  outline: 3px solid #F59E0B;
  outline-offset: 2px;
}

/* Icon Button */
.btn-icon {
  margin-right: 8px;
}

/* Sizes */
.pixel-button--sm {
  padding: 8px 16px;
  font-size: 0.625rem;
}

.pixel-button--md {
  padding: 12px 24px;
  font-size: 0.75rem;
}

.pixel-button--lg {
  padding: 16px 32px;
  font-size: 0.875rem;
}

/* States */
.pixel-button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.05) !important;
}

/* Focus Visible */
.pixel-button:focus-visible {
  outline: 3px solid #F59E0B;
  outline-offset: 2px;
}
</style>
