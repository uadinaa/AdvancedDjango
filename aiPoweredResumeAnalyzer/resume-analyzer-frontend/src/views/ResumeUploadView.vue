<template>
  <v-container>
    <v-card>
      <v-card-title>Upload Your Resume</v-card-title>
      <v-card-text>
        <v-file-input
          v-model="resumeFile"
          label="Select a resume (PDF/DOCX)"
          accept=".pdf,.doc,.docx"
          prepend-icon="mdi-upload"
        />

        <v-btn
          :loading="loading"
          color="primary"
          class="mt-3"
          @click="uploadResume"
        >
          Upload
        </v-btn>

        <v-alert
          v-if="message"
          type="success"
          class="mt-3"
          border="start"
        >
          {{ message }}
        </v-alert>
      </v-card-text>
    </v-card>

    <ResumeViewer class="mt-5" />
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import ResumeViewer from '@/components/Resumes/ResumeViewer.vue'

const resumeFile = ref(null)
const loading = ref(false)
const message = ref('')

const uploadResume = async () => {
  if (!resumeFile.value) return

  const formData = new FormData()
  formData.append('resume', resumeFile.value)

  loading.value = true
  try {
    await axios.post('/api/resumes/upload/', formData, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access')}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    message.value = 'Resume uploaded successfully!'
    resumeFile.value = null
  } catch (error) {
    message.value = 'Failed to upload resume.'
  } finally {
    loading.value = false
  }
}
</script>
