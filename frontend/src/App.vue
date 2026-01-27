<script setup lang="ts">
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

onMounted(async () => {
  if (authStore.isAuthenticated) {
    try {
      await authStore.fetchProfile();
    } catch (e: any) {
      // Only logout if it's a 401 Unauthorized or 403 Forbidden
      if (e.response && (e.response.status === 401 || e.response.status === 403)) {
         authStore.logout();
         router.push('/login');
      } else {
         console.warn("Fetch profile failed but keeping session:", e);
      }
    }
  }
});
</script>

<template>
  <router-view></router-view>
</template>

<style>
/* Global styles if needed */
</style>
