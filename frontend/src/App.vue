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
    } catch (e) {
      // Token invalid or session expired
      authStore.logout();
      router.push('/login');
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
