<template>
  <v-container>
    <h2 class="text-h5 font-weight-bold mb-4">Matched Jobs</h2>
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
    <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>

    <v-row v-if="jobs.length">
      <v-col v-for="job in jobs" :key="job.id" cols="12" md="6">
        <v-card>
          <v-card-title>{{ job.title }}</v-card-title>
          <v-card-subtitle>{{ job.company }}</v-card-subtitle>
          <v-card-text>{{ job.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      jobs: [],
      error: '',
      loading: false,
    }
  },
  mounted() {
    this.fetchMatches()
  },
  methods: {
    async fetchMatches() {
      this.loading = true
      try {
        const response = await axios.get('/api/job-match/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`
          }
        })
        this.jobs = response.data
      } catch (err) {
        this.error = 'Failed to load matched jobs.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
