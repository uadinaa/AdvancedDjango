<template>
  <v-container>
    <h2>Create a New Job</h2>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field
        v-model="job.title"
        label="Job Title"
        :rules="[v => !!v || 'Title is required']"
        required
      />

      <v-textarea
        v-model="job.description"
        label="Job Description"
        :rules="[v => !!v || 'Description is required']"
        required
      />

      <v-btn color="primary" @click="submitForm" :disabled="!valid">Create Job</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import jobService from '@/services/jobService';

export default {
  data() {
    return {
      valid: false,
      job: {
        title: '',
        description: ''
      }
    };
  },
  methods: {
    async submitForm() {
      if (this.$refs.form.validate()) {
        try {
          await jobService.createJob(this.job);
          this.$router.push('/jobs');
        } catch (err) {
          console.error(err);
        }
      }
    }
  }
};
</script>
