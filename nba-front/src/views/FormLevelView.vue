<script setup>
// import { onMounted } from 'vue'
import router from '@/router/index.js'

import { ref } from 'vue'

const expe1 = ref(50)
const expe2 = ref(50)

const nivel1 = ref('')
const nivel2 = ref('')

async function submit() {
  const payload = {
    expe1: expe1.value,
    nivel1: nivel1.value,
    expe2: expe2.value,
    nivel2: nivel2.value,
  }

  await fetch('http://localhost:5000/form', {
    credentials: 'include',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  await router.push('/etiquetar')
}
</script>

<template>
  <v-main class="bg-grey-lighten-4 d-flex justify-center align-center" style="height: 100vh">
    <v-card class="px-12 py-12 rounded-xl elevation-4 text-center" max-width="800" width="100%">
      <v-form>
        <!-- Título -->
        <h1 class="display-1 font-weight-bold mb-4">Primero, unas preguntas.</h1>
        <!-- Jugador -->
        <p>Años como jugador:</p>
        <v-slider v-model="expe1" thumb-label min="0" max="100" step="1"></v-slider>
        <p>¿A qué nivel?</p>
        <div class="d-flex justify-center ga-2 mt-2">
          <br />
          <v-row>
            <v-col class="py1" cols="12">
              <v-btn-toggle v-model="nivel1" multiple>
                <v-btn variant="tonal" color="#ffc04a">Local</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Autonómico</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Nacional</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Internacional</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Mundial</v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>
        </div>
        <br />
        <!-- Entrenador -->
        <p>Años como entrenador</p>
        <v-slider v-model="expe2" thumb-label min="0" max="100" step="1"></v-slider>
        <p>¿A qué nivel?</p>
        <div class="d-flex justify-center ga-2 mt-2">
          <br />
          <v-row>
            <v-col class="py2" cols="12">
              <v-btn-toggle v-model="nivel2" multiple>
                <v-btn variant="tonal" color="#ffc04a">Local</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Autonómico</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Nacional</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Internacional</v-btn>
                <v-btn variant="tonal" color="#ffc04a">Mundial</v-btn>
              </v-btn-toggle>
            </v-col>
          </v-row>
        </div>
        <br />
        <!-- Botón Empezar -->
        <v-btn color="#ffc04a" class="text-white px-8" large @click="submit">
          Empezar Etiquetado
        </v-btn>
      </v-form>
    </v-card>
  </v-main>
</template>

<style scoped></style>
