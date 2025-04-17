<template>
  <v-container>
    <v-card>
      <v-card-title>Reset Password</v-card-title>
      <v-card-text>
        <v-text-field v-model="email" label="Email" />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="requestReset">Send Reset Link</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axios from '@/axios'

export default {
  data() {
    return {
      email: ''
    }
  },
  methods: {
    async requestReset() {
      try {
        await axios.post('auth/password-reset/', { email: this.email })
        alert('Check your email for the reset link.')
      } catch {
        alert('Failed to send reset email.')
      }
    }
  }
}
</script>
