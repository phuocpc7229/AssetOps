import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: { name: 'dashboard' },
  },
  {
    path: '/assets',
    redirect: { name: 'assets' },
  },
  {
    path: '/assets/new',
    redirect: { name: 'asset-new' },
  },
  {
    path: '/assets/:id/edit',
    redirect: (to) => ({ name: 'asset-edit', params: to.params }),
  },
  {
    path: '/sites',
    redirect: { name: 'sites' },
  },
  {
    path: '/asset-types',
    redirect: { name: 'master-data', params: { kind: 'asset-types' } },
  },
  {
    path: '/vendors',
    redirect: { name: 'master-data', params: { kind: 'vendors' } },
  },
  {
    path: '/device-types',
    redirect: { name: 'master-data', params: { kind: 'device-types' } },
  },
  {
    path: '/locations',
    redirect: { name: 'master-data', params: { kind: 'locations' } },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: {
      title: 'Sign in',
    },
  },
  {
    path: '/',
    component: () => import('@/layouts/AppShell.vue'),
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/pages/DashboardPage.vue'),
        meta: {
          title: 'Dashboard',
        },
      },
      {
        path: 'dashboard/assets',
        name: 'assets',
        component: () => import('@/pages/AssetsPage.vue'),
        meta: {
          title: 'Assets',
        },
      },
      {
        path: 'dashboard/assets/new',
        name: 'asset-new',
        component: () => import('@/pages/AssetFormPage.vue'),
        meta: {
          title: 'Add Asset',
        },
      },
      {
        path: 'dashboard/assets/:id/edit',
        name: 'asset-edit',
        component: () => import('@/pages/AssetFormPage.vue'),
        meta: {
          title: 'Edit Asset',
        },
      },
      {
        path: 'dashboard/sites',
        name: 'sites',
        component: () => import('@/pages/SitesPage.vue'),
        meta: {
          title: 'Sites',
        },
      },
      {
        path: 'dashboard/master-data/:kind(asset-types|vendors|device-types|locations)',
        name: 'master-data',
        component: () => import('@/pages/MasterDataPage.vue'),
        meta: {
          title: 'Master Data',
        },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (authStore.isAuthenticated) {
    await authStore.loadCurrentUser()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'login' && authStore.isAuthenticated) {
    return { name: 'dashboard' }
  }
})

router.afterEach((to) => {
  const title = typeof to.meta.title === 'string' ? to.meta.title : 'AssetOps Portal'
  document.title = `${title} | AssetOps Portal`
})

export default router
