<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import HomeIcon from '@/components/icons/HomeIcon.vue'
import DishIcon from '@/components/icons/DishIcon.vue'
import CombinationIcon from '@/components/icons/CombinationIcon.vue'
import HistoryIcon from '@/components/icons/HistoryIcon.vue'

const router = useRouter()
const route = useRoute()

const navItems = [
  { path: '/', label: '首页', icon: 'home' },
  { path: '/dishes', label: '菜品', icon: 'dish' },
  { path: '/combinations', label: '搭配', icon: 'combination' },
  { path: '/history', label: '历史', icon: 'history' }
]

function navigate(path: string) {
  router.push(path)
}
</script>

<template>
  <!-- Desktop Header -->
  <header class="app-header desktop-header">
    <div class="container">
      <div class="header-content">
        <router-link to="/" class="logo">
          <dish-icon class="logo-icon" :size="32" />
          <span class="logo-text">家庭点菜</span>
        </router-link>

        <nav class="desktop-nav">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ 'router-link-active': route.path === item.path }"
          >
            <component
              :is="item.icon === 'home' ? HomeIcon : item.icon === 'dish' ? DishIcon : item.icon === 'combination' ? CombinationIcon : HistoryIcon"
              class="nav-icon"
              :size="20"
            />
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </nav>
      </div>
    </div>
  </header>

  <!-- Mobile Bottom Navigation -->
  <nav class="mobile-bottom-nav">
    <div
      v-for="item in navItems"
      :key="item.path"
      class="mobile-nav-item"
      :class="{ 'mobile-nav-item--active': route.path === item.path }"
      @click="navigate(item.path)"
    >
      <component
        :is="item.icon === 'home' ? HomeIcon : item.icon === 'dish' ? DishIcon : item.icon === 'combination' ? CombinationIcon : HistoryIcon"
        class="mobile-nav-icon"
        :size="24"
      />
      <span class="mobile-nav-label">{{ item.label }}</span>
    </div>
  </nav>
</template>

<style scoped>
/* Desktop Header */
.app-header {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border-bottom: 3px solid #1F2937;
  padding: 16px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #1F2937;
  font-size: 1.5rem;
  font-weight: bold;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: #F59E0B;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

/* Desktop Navigation */
.desktop-nav {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #6B7280;
  padding: 10px 20px;
  border: 3px solid transparent;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.5);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: -1;
}

.nav-link:hover {
  color: #1F2937;
  border-color: #1F2937;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.nav-link:hover::before {
  opacity: 1;
}

.nav-link.router-link-active {
  color: #1F2937;
  background: #F59E0B;
  border-color: #1F2937;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.nav-icon {
  width: 20px;
  height: 20px;
  color: currentColor;
  transition: color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 600;
}

/* Mobile Bottom Navigation */
.mobile-bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(180deg, rgba(254, 243, 199, 0.98) 0%, rgba(254, 243, 199, 1) 100%);
  border-top: 3px solid #1F2937;
  padding: 8px 0 env(safe-area-inset-bottom, 8px);
  z-index: 1000;
  backdrop-filter: blur(20px);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
}

.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 12px;
  position: relative;
}

.mobile-nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 40px;
  height: 3px;
  background: #F59E0B;
  border-radius: 2px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-nav-item--active::before {
  transform: translateX(-50%) scaleX(1);
}

.mobile-nav-icon {
  width: 24px;
  height: 24px;
  color: currentColor;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-nav-item--active .mobile-nav-icon {
  transform: scale(1.2);
  color: #F59E0B;
}

.mobile-nav-item:active .mobile-nav-icon {
  transform: scale(0.9);
}

.mobile-nav-label {
  font-size: 0.625rem;
  color: #6B7280;
  font-weight: 600;
  transition: color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-nav-item--active .mobile-nav-label {
  color: #1F2937;
}

/* Responsive */
@media (max-width: 768px) {
  .desktop-header {
    display: none;
  }

  .mobile-bottom-nav {
    display: flex;
    justify-content: space-around;
    align-items: center;
  }
}

@media (min-width: 769px) {
  .mobile-bottom-nav {
    display: none;
  }
}
</style>
