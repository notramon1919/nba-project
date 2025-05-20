<script setup>
import { onMounted } from 'vue'
import router from '@/router/index.js'

onMounted(() => {
  // Si no está completado, redirigir a login
  const completado = sessionStorage.getItem('etiquetado_completo')
  if (completado !== 'true') {
    router.push('/login')
  }
})

function volver_clicked() {
  sessionStorage.setItem('etiquetado_completo', 'false')
  router.push('/login')
}
</script>

<template>
  <v-main class="bg-grey-lighten-4 d-flex justify-center align-center" style="height: 100vh">
    <v-card class="px-12 py-12 rounded-xl elevation-4 text-center" max-width="600" width="100%">
      <!-- Icono hecho -->
      <v-icon size="120" color="success" class="mb-6">mdi-check-circle-outline</v-icon>

      <!-- Título -->
      <h1 class="display-1 font-weight-bold mb-4">¡Experimento Completado!</h1>

      <!-- Texto -->
      <p class="text-subtitle-1 mb-8">
        Gracias por tu colaboración. Tus etiquetas se han guardado con exitosamente.
      </p>

      <!-- Botón Volver al Inicio -->
      <v-btn color="#ffc04a" class="text-white px-8" large @click="volver_clicked">
        Volver al Inicio
      </v-btn>
    </v-card>
  </v-main>
</template>

<style scoped></style>
