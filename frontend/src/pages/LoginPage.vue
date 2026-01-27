<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const authStore = useAuthStore();
const router = useRouter();
const error = ref('');
const isLoading = ref(false);

const bgImage = computed(() => {
    return `url('/login.jpg')`;
});

const handleLogin = async () => {
  error.value = '';
  isLoading.value = true;
  try {
    await authStore.login({ username: username.value, password: password.value });
    if (authStore.isAdmin) {
        router.push('/admin');
    } else {
        router.push('/order');
    }
  } catch (e) {
    error.value = 'Invalid credentials';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 bg-cover bg-center bg-no-repeat bg-fixed" 
       :style="{ backgroundImage: bgImage }">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-lg shadow-2xl w-full max-w-md">
      <h2 class="text-3xl font-bold text-center text-navy-blue mb-6">Login</h2>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
           <label class="block text-gray-700 font-semibold">Username</label>
           <input v-model="username" type="text" class="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-saffron outline-none transition-all" required :disabled="isLoading" />
        </div>
        <div>
           <label class="block text-gray-700 font-semibold">Password</label>
           <input v-model="password" type="password" class="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-saffron outline-none transition-all" required :disabled="isLoading" />
        </div>
        <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
        <button type="submit" class="w-full bg-saffron text-white py-2 rounded hover:bg-orange-600 transition-colors font-semibold shadow-md flex justify-center items-center" :disabled="isLoading">
            <span v-if="isLoading" class="animate-spin h-5 w-5 mr-3 border-t-2 border-b-2 border-white rounded-full"></span>
            {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <div class="mt-4 text-center">
        <a href="/register" class="text-navy-blue hover:underline">Create an account</a>
        <span class="mx-2">|</span>
        <a href="/" class="text-gray-500 hover:text-gray-700">Back to Home</a>
      </div>
    </div>
  </div>
</template>
