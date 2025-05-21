<script setup>
import { onMounted } from 'vue'
import router from '@/router/index.js'

onMounted(() => {})

function empezar() {
  router.push('/etiquetar')
}
</script>

<template>
  <v-main class="bg-grey-lighten-4 d-flex justify-center align-center" style="height: 100vh">
    <v-card class="px-12 py-12 rounded-xl elevation-4 text-center" max-width="800" width="100%">
      <!-- Título -->
      <h1 class="display-1 font-weight-bold mb-4">Primero, unas preguntas.</h1>

      <!-- Texto -->
      <p class="text-subtitle-1 mb-8">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi aperiam aspernatur
        consectetur consequuntur delectus ducimus esse fugiat illum in inventore maiores, molestias
        nemo officiis omnis possimus reiciendis, sed ut vitae!

        <br />

        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi aperiam aspernatur
        consectetur consequuntur delectus ducimus esse fugiat illum in inventore maiores, molestias
        nemo officiis omnis possimus reiciendis, sed ut vitae!

        <br />

        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi aperiam aspernatur
        consectetur consequuntur delectus ducimus esse fugiat illum in inventore maiores, molestias
        nemo officiis omnis possimus reiciendis, sed ut vitae!

        <br />

        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi aperiam aspernatur
        consectetur consequuntur delectus ducimus esse fugiat illum in inventore maiores, molestias
        nemo officiis omnis possimus reiciendis, sed ut vitae!

        <br />
      </p>

      <!-- Botón Empezar -->
      <v-btn color="#ffc04a" class="text-white px-8" large @click="empezar">
        Empezar Etiquetado
      </v-btn>
    </v-card>
  </v-main>
</template>

<style scoped></style>
