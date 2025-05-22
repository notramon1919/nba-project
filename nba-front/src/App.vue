<script setup>
import { RouterView } from 'vue-router'
import { ref } from 'vue'

const informacion = ref(false)
</script>

<template>
  <v-app>
    <!-- Dialog -->
    <v-dialog v-model="informacion" max-width="600">
      <v-card class="px-12 py-12 rounded-xl elevation-4">
        <v-card-title> Información</v-card-title>

        <v-card-text>
          App realizada por <a href=""> Ramón Martí</a> en colaboración con
          <a href="">Alberto Martí</a>.
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Botón flotante fijo -->
    <v-btn icon class="fixed-button" color="#ffc04a" @click="informacion = true">
      <v-icon size="36" color="white">mdi-information-variant</v-icon>
    </v-btn>

    <!-- Vistas -->
    <RouterView />
  </v-app>
</template>

<style scoped>
.fixed-button {
  position: fixed;
  top: 30px;
  right: 30px;
  z-index: 1000;
  width: 64px;
  height: 64px;
}
</style>
