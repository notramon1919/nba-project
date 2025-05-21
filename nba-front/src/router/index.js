import { createRouter, createWebHistory } from 'vue-router'
import EtiquetarView from '@/views/EtiquetarView.vue'
import LoginView from '@/views/LoginView.vue'
import CompletadoView from '@/views/CompletadoView.vue'
import FormLevelView from '@/views/FormLevelView.vue'

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
      path: '/completado',
      name: 'CompletadoView',
      component: CompletadoView,
    },
    {
      path: '/form',
      name: 'FormView',
      component: FormLevelView
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login',
    },
  ],
})

export default router

router.beforeEach((to, from, next) => {
  const user = sessionStorage.getItem('user')
  const completado = sessionStorage.getItem('etiquetado_completo')

  if (!user && to.meta.requiresAuth) {
    // Si no ha iniciado sesión y la ruta requiere auth, redirige al login
    next({ name: 'LoginView' })
  } else if (to.path === '/etiquetar' && completado === 'true') {
    // Si ya completó y quiere volver a etiquetar, lo mandamos a completado
    next({ name: 'CompletadoView' })
  } else {
    // Lo demás permitido
    next()
  }
})
