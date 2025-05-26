<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <v-app>
    <!-- Contenido principal -->
    <v-main class="d-flex flex-column">
      <RouterView />
    </v-main>

    <!-- Footer -->
    <v-footer class="bg-grey-lighten-3 text-center" height="auto" app>
      <v-container>
        <span class="text-grey-darken-2"
          >&copy; 2025 - App hecha por <a href="">Ramón Martí</a> y
          <a href="">Alberto Martí</a>
        </span>
        <!-- Imagen Init y UJI -->
        <v-img
          class="mx-auto mt-4"
          style="width: 400px"
          src="src/assets/images/pie-pagina-escalado.png"
        />
      </v-container>
    </v-footer>
  </v-app>
</template>
