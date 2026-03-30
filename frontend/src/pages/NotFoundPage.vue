<script setup lang="ts">
// 404 Not Found Page
</script>

<template>
  <div class="not-found-page">
    <div class="container">
      <div class="error-content">
        <h1>4️⃣0️⃣4️⃣</h1>
        <h2>页面未找到</h2>
        <p>抱歉，您访问的页面不存在</p>
        <router-link to="/" class="home-link">返回首页</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  text-align: center;
}

.error-content h1 {
  font-size: 4rem;
  margin-bottom: 1rem;
  color: var(--color-coral-400);
}

.error-content h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.home-link {
  display: inline-block;
  margin-top: 1.5rem;
  padding: 12px 24px;
  background: var(--color-amber-500);
  color: #1F2937;
  text-decoration: none;
  border: 2px solid #1F2937;
  transition: transform 0.15s;
}

.home-link:hover {
  transform: scale(1.05);
}
</style>
