<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card class="pa-5 text-center" elevation="4" max-width="400">
      <v-card-title class="headline">403 - Access Denied</v-card-title>
      <v-card-text>
        You don’t have permission to view this page.
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn color="primary" @click="$router.push('/')">
          Go Home
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'NotAuthorized'
}
</script>
