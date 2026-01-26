<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import { v4 as uuidv4 } from 'uuid';

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const emailError = ref('');
const generalError = ref('');
const authStore = useAuthStore();
const router = useRouter();

const getDeviceId = () => {
  let deviceId = localStorage.getItem('device_id');
  if (!deviceId) {
    deviceId = uuidv4();
    localStorage.setItem('device_id', deviceId);
  }
  return deviceId;
};

const validateEmail = () => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.value) return;
  if (!re.test(email.value)) {
    emailError.value = "Invalid email format";
  } else {
    emailError.value = "";
  }
};

const handleRegister = async () => {
  generalError.value = "";
  if (password.value.length < 8) {
    generalError.value = "Password must be at least 8 characters long.";
    return;
  }
  if (password.value !== confirmPassword.value) {
    generalError.value = "Passwords do not match";
    return;
  }
  if (emailError.value) return;

  try {
    const deviceId = getDeviceId();
    await authStore.register({ 
        username: username.value, 
        email: email.value, 
        password: password.value,
        confirm_password: confirmPassword.value,
        registration_cookie: deviceId
    });
    // Auto login or redirect to login
    await authStore.login({ username: username.value, password: password.value });
    router.push('/order');
  } catch (e: any) {
    if (e.response && e.response.data && e.response.data.detail) {
        generalError.value = e.response.data.detail;
    } else {
        generalError.value = 'Registration failed. Username might be taken.';
    }
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-cover bg-center" style="background-image: url('https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=India%20Landscape%20Business%20Sunrise&image_size=landscape_16_9')">
    <div class="bg-white/90 backdrop-blur-md p-8 rounded-lg shadow-2xl w-full max-w-md">
      <h2 class="text-3xl font-bold text-center text-navy-blue mb-6">Register</h2>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
           <label class="block text-gray-700 font-semibold">Username</label>
           <input v-model="username" type="text" class="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-saffron outline-none transition-all" required />
        </div>
        <div>
           <label class="block text-gray-700 font-semibold">Email</label>
           <input v-model="email" @blur="validateEmail" type="email" class="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-saffron outline-none transition-all" required />
           <p v-if="emailError" class="text-red-500 text-xs mt-1">{{ emailError }}</p>
        </div>
        <div>
           <label class="block text-gray-700 font-semibold">Password</label>
           <input v-model="password" type="password" class="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-saffron outline-none transition-all" required />
        </div>
        <div>
           <label class="block text-gray-700 font-semibold">Confirm Password</label>
           <input v-model="confirmPassword" type="password" class="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-saffron outline-none transition-all" required />
        </div>
        <p v-if="generalError" class="text-red-500 text-sm text-center">{{ generalError }}</p>
        <button type="submit" class="w-full bg-saffron text-white py-2 rounded hover:bg-orange-600 transition-colors font-semibold shadow-md">Sign Up</button>
      </form>
      <div class="mt-4 text-center">
        <a href="/login" class="text-navy-blue hover:underline">Already have an account? Login</a>
        <span class="mx-2">|</span>
        <a href="/" class="text-gray-500 hover:text-gray-700">Back to Home</a>
      </div>
    </div>
  </div>
</template>
