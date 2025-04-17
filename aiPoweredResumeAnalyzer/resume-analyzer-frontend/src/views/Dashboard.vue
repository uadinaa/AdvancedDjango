/* eslint-disable vue/multi-word-component-names */

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Welcome, {{ role }}</span>
        <v-btn color="error" @click="logout" small>Logout</v-btn>
      </v-card-title>
      <v-divider></v-divider>

      <!-- Resume Upload Section -->
      <v-row class="mt-4">
        <v-col cols="12" sm="6" md="4">
          <v-card>
            <v-card-title>Upload Your Resume</v-card-title>
            <v-card-text>
              <v-file-input
                v-model="resumeFile"
                label="Choose a resume file"
                accept=".pdf,.docx"
                outlined
              />
            </v-card-text>
            <v-card-actions>
              <v-btn @click="uploadResume" color="primary" block>Upload Resume</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Role-based Button Display -->
      <v-row class="mt-4">
        <v-col cols="12" sm="6" md="4" v-if="role === 'user'">
          <v-btn block color="primary" to="/job-match-results">View Job Matches</v-btn>
          <v-btn block color="secondary" to="/feedback">View AI Feedback</v-btn>
        </v-col>

        <v-col cols="12" sm="6" md="4" v-else-if="role === 'admin'">
          <v-btn block color="primary" to="/admin">Admin Dashboard</v-btn>
          <v-btn block color="info" to="/admin/user-list">Manage Users</v-btn>
        </v-col>

        <v-col cols="12" sm="6" md="4" v-else-if="role === 'recruiter'">
          <v-btn block color="success" to="/admin/job-list">Post Jobs</v-btn>
        </v-col>
      </v-row>

      <!-- Common Actions -->
<v-row class="mt-4">
  <!-- View All Jobs -->
  <v-col cols="12" sm="6" md="4">
    <v-btn block color="primary" to="/jobs">View All Jobs</v-btn>
  </v-col>

  <!-- View All Resumes -->
  <v-col cols="12" sm="6" md="4">
    <v-btn block color="secondary" to="/resumes">View All Resumes</v-btn>
  </v-col>

  <!-- Analyze Resume -->
  <v-col cols="12" sm="6" md="4">
    <v-btn block color="info" to="/analyze-resume">Analyze Resume</v-btn>
  </v-col>

  <!-- Feedback -->
  <v-col cols="12" sm="6" md="4">
    <v-btn block color="success" to="/feedback">AI Feedback</v-btn>
  </v-col>

  <!-- Match Page -->
  <v-col cols="12" sm="6" md="4">
    <v-btn block color="warning" to="/job-match-results">Job Match</v-btn>
  </v-col>

  <!-- Admin Only: View Users -->
  <v-col cols="12" sm="6" md="4" v-if="role === 'admin'">
    <v-btn block color="error" to="/admin/user-list">User List</v-btn>
  </v-col>
</v-row>



    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ResumeDashboard',
  data() {
    return {
      role: localStorage.getItem('role'),
      resumeFile: null
    }
  },
  methods: {
    async uploadResume() {
      if (!this.resumeFile) {
        alert('Please choose a file to upload.');
        return;
      }

      const formData = new FormData();
      formData.append('resume', this.resumeFile);

      try {
        const response = await axios.post('/api/resumes/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('access')}`
          }
        });

        if (response.status === 200) {
          alert('Resume uploaded successfully!');
        } else {
          alert('Failed to upload resume.');
        }
      } catch (error) {
        alert('Error uploading resume: ' + error.message);
      }
    },
    logout() {
      localStorage.removeItem('access');
      localStorage.removeItem('role');
      this.$router.push('/login');
    }
  }
}
</script>
