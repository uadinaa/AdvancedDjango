<template>
  <v-container>
    <h2 class="text-h5 font-weight-bold mb-4">AI Feedback on Your Resume</h2>
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
    <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>

    <v-card v-if="feedback" class="pa-4">
      <div v-html="feedback.text"></div>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserFeedback',
  data() {
    return {
      feedback: null,
      error: '',
      loading: false
    }
  },
  mounted() {
    this.getFeedback()
  },
  methods: {
    async getFeedback() {
      this.loading = true
      try {
        const res = await axios.get('/api/resume-feedback/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`
          }
        })
        this.feedback = res.data
      } catch (err) {
        this.error = 'Could not fetch feedback.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
