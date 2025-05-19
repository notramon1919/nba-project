<script setup>
import { ref, computed } from 'vue'

const gifs = ref([])
const currentIndex = ref(0)
const gifActual = computed(() => gifs.value[currentIndex.value] || '')

const valido_novalido = ref(null)
const gif_features_text = ref('')
const progress = computed(() => (currentIndex.value / gifs.value.length) * 100)
const disabled = computed(() => valido_novalido.value === null)

async function fetchGifs() {
  const response = await fetch('http://localhost:5000/gifs')
  const data = await response.json()
  gifs.value = data.gifs
}
fetchGifs()

async function execute_submit() {

  if (!gifActual.value) return

  setTimeout(() => {
    valido_novalido.value = null
    gif_features_text.value = ''
  }, 1)

  const payload = {
    gif: gifActual.value,
    valido: valido_novalido.value,
    descripcion: gif_features_text.value,
    etiquetado_por: "Persona1"
  }

  await fetch('http://localhost:5000/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  currentIndex.value += 1
}
</script>

<template>
  <v-container class="d-flex flex-column align-center">

    <!-- Barra de Progreso -->
    <v-progress-linear
      class="mb-16"
      :model-value="progress"
      color="#29b8c4"
      style="width: 65%; height: 25px"
      rounded
    >
      <template v-slot:default="{ value }">
        <strong>{{ Math.round(value) }}%</strong>
      </template>
    </v-progress-linear>

    <!-- Imagen -->
    <v-img
      v-if="gifActual"
      :src="`http://localhost:5000/static/${gifActual}`"
      width="600"
      max-height="450"
      class="mb-6"
    />

    <!-- Botones de válido / no válido -->
    <v-row no-gutters style="width: 100%; max-width: 650px; margin-top: 40px">
      <v-btn-toggle v-model="valido_novalido" mandatory style="width: 100%">
        <v-col cols="6" class="pa-1">

          <!-- Válido -->
          <v-btn
            id="btn"
            :value="true"
            block
            variant="tonal"
            prepend-icon="mdi-check"
            color="#34bf37"
            elevation="2"
            style="height: 100%"
          >
            Es Válido
          </v-btn>
        </v-col>

        <v-col cols="6" class="pa-1">

          <!-- No Válido -->
          <v-btn
            id="btn"
            :value="false"
            block
            variant="tonal"
            prepend-icon="mdi-close"
            color="#de2a2a"
            elevation="2"
            style="height: 100%"
            @click="execute_submit"
          >
            No Es Válido
          </v-btn>
        </v-col>
      </v-btn-toggle>
    </v-row>

    <!-- TextArea -->
    <v-textarea
      class="mt-4"
      v-model="gif_features_text"
      label="Descripción"
      maxlength="250"
      counter
      rows="5"
      variant="outlined"
      :disabled="disabled"
      style="max-width: 650px; width: 100%;"
    />

    <!-- Botón Confirmar -->
    <div class="d-flex justify-center mt-4">
      <v-btn
        id="btn"
        prepend-icon="mdi-upload"
        width="200px"
        :disabled="disabled"
        @click="execute_submit"
      >
        Confirmar
      </v-btn>
    </div>
  </v-container>
</template>

<style scoped>
#btn {
  font-weight: 650 !important;
}
</style>
