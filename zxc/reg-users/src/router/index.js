import { createRouter, createWebHistory } from 'vue-router'

const routes = [
	{
		path: '/',
		name: 'login',
		meta: {layout: 'empty'},
		component: () => import('@/views/LoginPage.vue')
	},
	{
		path: '/register',
		name: 'register',
		meta: {layout: 'empty'},
		component: () => import('@/views/RegisterPage.vue')
	},
  {
    path: '/main',
    name: 'home',
		meta: {layout: 'main'},
    component: () => import('@/views/MainPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
