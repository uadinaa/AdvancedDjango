<template>
  <v-card>
    <v-card-title>Parsed Resume (Raw Text)</v-card-title>
    <v-card-text>
      <v-skeleton-loader v-if="loading" type="paragraph" />
      <div v-else>
        <pre style="white-space: pre-wrap;">{{ resumeText }}</pre>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const resumeText = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('/api/resumes/me/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`
      }
    })
    resumeText.value = res.data.raw_text || 'No parsed resume found.'
  } catch (err) {
    resumeText.value = 'Error fetching resume.'
  } finally {
    loading.value = false
  }
})
</script>


<template>
  <v-container class="mt-6">
    <v-card class="pa-4">
      <v-card-title class="text-h6">Resume Preview</v-card-title>
      <v-divider></v-divider>
      <v-card-text v-if="resume">
        <div class="mb-2"><strong>Name:</strong> {{ resume.name }}</div>
        <div class="mb-2"><strong>Email:</strong> {{ resume.email }}</div>
        <div class="mb-2"><strong>Phone:</strong> {{ resume.phone }}</div>

        <div v-if="resume.education" class="mb-4">
          <strong>Education:</strong>
          <ul>
            <li v-for="(edu, index) in resume.education" :key="index">
              {{ edu.degree }} - {{ edu.institution }} ({{ edu.year }})
            </li>
          </ul>
        </div>

        <div v-if="resume.experience">
          <strong>Experience:</strong>
          <ul>
            <li v-for="(exp, index) in resume.experience" :key="index">
              {{ exp.position }} at {{ exp.company }} ({{ exp.years }})
            </li>
          </ul>
        </div>
      </v-card-text>
      <v-card-text v-else>
        No resume data available.
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'ResumeViewer',
  props: {
    resume: {
      type: Object,
      required: false,
      default: () => null
    }
  }
}
</script>

<style scoped>
ul {
  padding-left: 1rem;
}
</style>
