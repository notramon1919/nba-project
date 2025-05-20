import { createRouter, createWebHistory } from 'vue-router'
import EtiquetarView from '@/views/EtiquetarView.vue'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/etiquetar',
      name: 'EtiquetarView',
      component: EtiquetarView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ],
})

export default router

// Guard global para proteger rutas con meta.requiresAuth
router.beforeEach((to, from, next) => {
  const user = sessionStorage.getItem('user') // Usuario guardado en sessionStorage

  if (to.meta.requiresAuth && !user) {
    next({ name: 'LoginView' })
  } else {
    // Si está logueado o la ruta no está protegida, continúa
    next()
  }
})
