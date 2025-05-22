<script setup>
import { onMounted } from 'vue'
import router from '@/router/index.js'

onMounted(() => {})

function empezar() {
  router.push('/etiquetar')
}

import { ref } from 'vue'

const slider1 = ref(50)
const slider2 = ref(50)
</script>

<template>
  <v-main class="bg-grey-lighten-4 d-flex justify-center align-center" style="height: 100vh">
    <v-card class="px-12 py-12 rounded-xl elevation-4 text-center" max-width="800" width="100%">
      <!-- Título -->
      <h1 class="display-1 font-weight-bold mb-4">Primero, unas preguntas.</h1>
      <!-- Primer Slider -->
      <v-container>
        <p>Años como jugador:</p>
        <v-slider v-model="slider1" thumb-label min="0" max="100" step="1"></v-slider>
        <p>Años como entrenador</p>
        <v-slider v-model="slider2" thumb-label min="0" max="100" step="1"></v-slider>
      </v-container>
      <!-- Texto -->

      <!-- Botón Empezar -->
      <v-btn color="#ffc04a" class="text-white px-8" large @click="empezar">
        Empezar Etiquetado
      </v-btn>
    </v-card>
  </v-main>
</template>

<style scoped></style>
