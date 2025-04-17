<template>
  <v-container>
    <v-alert type="info">Verifying email...</v-alert>
  </v-container>
</template>

<script>
import axios from '@/axios'

export default {
  async mounted() {
    const token = this.$route.query.token
    try {
      await axios.post('auth/verify-email/', { token })
      alert('Email verified! You can now log in.')
      this.$router.push('/login')
    } catch {
      alert('Verification failed.')
    }
  }
}
</script>
