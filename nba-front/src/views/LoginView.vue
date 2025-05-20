<script setup>
import { ref } from 'vue'
import router from '@/router/index.js'

const snackbar_login_completado = ref(false)
const snackbar_login_error = ref(false)
const error_msg = ref('')

const form = ref(false)
const username = ref('')
const password = ref('')
const loading = ref(false)

function required(v) {
  return !!v || 'Field is required'
}

async function onSubmit() {
  if (!form.value) return
  loading.value = true

  try {
    const res = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })

    const data = await res.json()

    if (res.ok && data.success) {
      snackbar_login_completado.value = true
      error_msg.value = ''
      sessionStorage.setItem('user', data.user)
      await router.push('/etiquetar')
    } else {
      snackbar_login_error.value = true
      error_msg.value = data.message || 'Error al iniciar sesión'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-main class="bg-grey-lighten-4 d-flex align-center justify-center" style="min-height: 100vh">
    <v-card class="px-12 py-12 rounded-xl elevation-4" width="344">
      <v-form v-model="form" @submit.prevent="onSubmit">
        <!-- Username -->
        <v-text-field
          v-model="username"
          :readonly="loading"
          :rules="[required]"
          class="mb-2"
          label="Username"
        ></v-text-field>

        <!-- Contraseña -->
        <v-text-field
          v-model="password"
          :readonly="loading"
          type="password"
          :rules="[required]"
          label="Password"
          placeholder="Enter your password"
        ></v-text-field>

        <!-- Botón Iniciar Sesión -->
        <v-btn
          :disabled="!form || loading"
          :loading="loading"
          color="#ffc04a"
          class="text-white px-6"
          size="large"
          type="submit"
          variant="elevated"
          block
        >
          Iniciar Sesión
        </v-btn>
      </v-form>
    </v-card>
  </v-main>

  <!-- Snackbars -->
  <v-snackbar v-model="snackbar_login_completado" :timeout="2000" color="success" location="left">
    Login exitoso
  </v-snackbar>

  <v-snackbar v-model="snackbar_login_error" :timeout="3000" color="error" location="left">
    {{ error_msg }}
  </v-snackbar>
</template>
