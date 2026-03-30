import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/pages/HomePage.vue'),
      meta: { title: '今日菜单' }
    },
    {
      path: '/dishes',
      name: 'dishes',
      component: () => import('@/pages/DishesPage.vue'),
      meta: { title: '菜品管理' }
    },
    {
      path: '/dishes/:id',
      name: 'dish-detail',
      component: () => import('@/pages/DishDetailPage.vue'),
      meta: { title: '菜品详情' }
    },
    {
      path: '/combinations',
      name: 'combinations',
      component: () => import('@/pages/CombinationsPage.vue'),
      meta: { title: '搭配清单' }
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/pages/HistoryPage.vue'),
      meta: { title: '历史记录' }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/pages/NotFoundPage.vue'),
      meta: { title: '页面未找到' }
    }
  ],
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || '家庭点菜系统'} - 家庭点菜`
  next()
})

export default router
