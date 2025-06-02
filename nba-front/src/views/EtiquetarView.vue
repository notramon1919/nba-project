<script setup>
import { ref, computed, watch } from 'vue'
import router from '@/router/index.js'

const imagenCargando = ref(true)
const gifs = ref([])
const currentIndex = ref(0)
const gifActual = computed(() => gifs.value[currentIndex.value] || '')

const valido_novalido = ref(null)
const gif_features_text = ref('')
const progress = computed(() => (currentIndex.value / 30) * 100)
const disabled = computed(() => valido_novalido.value === null)
const equipo = ref(null)

function handleImageLoad() {
  imagenCargando.value = false
}

function equipoAleatorio() {
  equipo.value = Math.random() < 0.5 ? 'rojo' : 'azul'
}

async function fetchGifs() {
  const response = await fetch('/gifs', {
    method: 'GET',
    credentials: 'include',
  })
  const data = await response.json()
  console.log('GIFs recibidos del backend:', data.gifs)
  gifs.value = data.gifs
}

equipoAleatorio()
fetchGifs()

async function execute_submit() {
  if (!gifActual.value) return

  const payload = {
    gif: gifActual.value,
    valido: valido_novalido.value,
    descripcion: gif_features_text.value,
    equipo: equipo.value,
    etiquetado_por: sessionStorage.getItem('user')  }

  await fetch('/submit', {
    credentials: 'include',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  valido_novalido.value = null
  gif_features_text.value = ''
  currentIndex.value += 1
  equipoAleatorio()

  if (currentIndex.value >= 30) {
    sessionStorage.setItem('etiquetado_completo', 'true')
    await router.push('/completado')
  }
}

watch(gifActual, () => {
  imagenCargando.value = true
})

</script>

<template>
  <v-main class="bg-grey-lighten-4 d-flex justify-center align-center">
    <v-card class="px-10 py-10 rounded-xl elevation-4 mt-16" max-width="700" width="100%">
      <!-- Barra de Progreso -->
      <v-progress-linear :model-value="progress" height="25" color="#ffc04a" rounded class="mb-4">
        <template v-slot:default="{ value }">
          <strong>{{ Math.round(value) }}%</strong>
        </template>
      </v-progress-linear>

      <!-- Texto color equipo -->
      <p style="text-align: center; margin-bottom: 10px; font-size: 24px" class="rounded">
        Si la jugada es válida, describe al equipo
        <strong :class="{ 'equipo-rojo': equipo === 'rojo', 'equipo-azul': equipo === 'azul' }">
          {{ equipo }}</strong
        >.
      </p>

      <div style="position: relative; max-height: 300px;" class="mb-2">
        <div
          v-if="imagenCargando"
          class="position-absolute w-100 h-100 d-flex flex-column justify-center align-center"
          style="background-color: rgba(255, 255, 255, 0.85); z-index: 2;"
        >
          <v-progress-circular indeterminate color="#ffc04a" size="64"/>
          <div class="mt-4 text-subtitle-1 font-weight-medium">Cargando Imagen...</div>
        </div>

        <!-- Imagen -->
        <v-img
          v-if="gifActual"
          :src="'/' + gifActual"
          max-height="300"
          aspect-ratio="16/9"
          class="rounded mb-2"
          @load="handleImageLoad"
          @error="handleImageLoad"
        />
      </div>

      <!-- Botones Válido / No Válido -->
      <v-btn-toggle
        v-model="valido_novalido"
        mandatory
        class="d-flex justify-space-between mb-6"
        style="width: 100%"
      >
        <v-btn
          :value="true"
          variant="elevated"
          prepend-icon="mdi-check"
          color="success"
          style="width: 49%"
          base-color="#f5f5f5"
        >
          Es Válido
        </v-btn>
        <v-btn
          :value="false"
          variant="elevated"
          prepend-icon="mdi-close"
          color="error"
          style="width: 49%"
          base-color="#f5f5f5"
          @click="execute_submit"
        >
          No es Válido
        </v-btn>
      </v-btn-toggle>

      <!-- Textarea -->
      <v-textarea
        v-model="gif_features_text"
        label="Descripción del GIF"
        counter
        maxlength="250"
        rows="3"
        variant="outlined"
        :disabled="disabled"
      />

      <!-- Confirmar -->
      <div class="text-center">
        <v-btn
          prepend-icon="mdi-upload"
          color="#ffc04a"
          class="text-white px-6"
          :disabled="disabled"
          @click="execute_submit"
        >
          Confirmar
        </v-btn>
      </div>
    </v-card>
  </v-main>
</template>

<style scoped>
.equipo-rojo {
  background-color: red;
  color: white;
  font-weight: 800;
  padding: 4px 8px;
  border-radius: 12px;
  display: inline-block;
}

.equipo-azul {
  background-color: blue;
  color: white;
  font-weight: 800;
  padding: 4px 8px;
  border-radius: 12px;
  display: inline-block;
}

</style>
