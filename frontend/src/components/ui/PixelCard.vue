<script setup lang="ts">
defineProps<{
  hoverable?: boolean
  padding?: 'sm' | 'md' | 'lg'
}>()

defineEmits<{
  click: []
}>()
</script>

<template>
  <div
    class="pixel-card"
    :class="[
      `pixel-card--padding-${padding || 'md'}`,
      { 'pixel-card--hoverable': hoverable }
    ]"
    @click="$emit('click')"
  >
    <slot />
  </div>
</template>

<style scoped>
.pixel-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
  border: 3px solid #1F2937;
  border-radius: 16px;
  box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.pixel-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(254, 243, 199, 0.3) 0%, rgba(253, 230, 138, 0.2) 100%);
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}

.pixel-card--hoverable {
  cursor: pointer;
}

.pixel-card--hoverable:hover {
  transform: translateY(-4px);
  box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.15);
}

.pixel-card--hoverable:hover::before {
  opacity: 1;
}

.pixel-card--hoverable:active {
  transform: translateY(0);
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.1);
}

/* Padding Sizes */
.pixel-card--padding-sm {
  padding: 16px;
}

.pixel-card--padding-md {
  padding: 24px;
}

.pixel-card--padding-lg {
  padding: 32px;
}

/* Focus Visible */
.pixel-card:focus-visible {
  outline: 3px solid #F59E0B;
  outline-offset: 2px;
}
</style>
