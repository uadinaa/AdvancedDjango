<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="headline">{{ job.title }}</v-card-title>
      <v-card-text>
        <p><strong>Description:</strong></p>
        <p>{{ job.description }}</p>
      </v-card-text>

      <v-card-actions v-if="canEdit">
        <v-btn color="primary" @click="editJob">Edit</v-btn>
        <v-btn color="error" @click="deleteJob">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import jobService from '@/services/jobService';
// import auth from '@/services/auth'
import { hasRole } from '@/services/auth'
// import { auth } from '@/services/auth'
import { user } from '@/services/auth'






export default {
  data() {
    return {
      job: {},
      canEdit: false
    };
  },
  async created() {
    const id = this.$route.params.id;

    try {
      const res = await jobService.getJobById(id);
      this.job = res.data;

      // const user = auth.getUser();
      this.canEdit = hasRole(['admin', 'recruiter']);
      this.canEdit = user && (user.role === 'admin' || user.role === 'recruiter');
    } catch (err) {
      console.error('Failed to fetch job detail:', err);
    }
  },
  methods: {
    editJob() {
      this.$router.push(`/jobs/${this.job.id}/edit`);
    },
    async deleteJob() {
      if (confirm('Are you sure you want to delete this job?')) {
        try {
          await jobService.deleteJob(this.job.id);
          this.$router.push('/jobs');
        } catch (err) {
          console.error('Error deleting job:', err);
        }
      }
    }
  }
};
</script>
