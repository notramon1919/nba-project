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
    <v-footer class="bg-grey-lighten-3 text-center" height="135px" app>
      <v-container>
        <span class="text-grey-darken-2"
          >&copy; 2025 - App hecha por
          <a target="_blank" href="https://www.linkedin.com/in/ramón-martí-adsuara">Ramón Martí</a>
          y
          <a target="_blank" href="https://www.linkedin.com/in/alberto-mart%C3%AD-llorens-7639082aa/">Alberto Martí</a>
        </span>
        <!-- Imagen Init y UJI -->
        <v-img
          class="mx-auto"
          style="width: 400px"
          src="src/assets/images/pie-pagina-escalado.png"
        />
      </v-container>
    </v-footer>
  </v-app>
</template>
