<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { Plus, Info, AlertCircle, CheckCircle, Clock, XCircle } from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();

const orders = ref<any[]>([]);
const isModalOpen = ref(false);
const isRechargeModalOpen = ref(false);
const isDetailModalOpen = ref(false);
const selectedOrder = ref<any>(null);

const newTask = ref({
  video_type: 'video',
  video_link: '',
  title: '',
  quantity: 100
});

const formError = ref('');

const fetchOrders = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/orders/');
    orders.value = response.data;
  } catch (e) {
    console.error(e);
  }
};

const openCreateModal = () => {
  isModalOpen.value = true;
};

const submitTask = async () => {
  if (!newTask.value.video_link || !newTask.value.title || !newTask.value.quantity) {
    formError.value = "All fields are required";
    return;
  }
  
  const cost = newTask.value.quantity * 2;
  if (authStore.user.balance < cost) {
    formError.value = `Insufficient balance. Cost: ₹${cost}, Balance: ₹${authStore.user.balance}`;
    return;
  }

  try {
    const task_id = 'TASK-' + Date.now();
    await axios.post('http://localhost:8000/api/orders/', {
      ...newTask.value,
      task_id
    });
    isModalOpen.value = false;
    await fetchOrders();
    // Refresh profile to update balance
    await authStore.fetchProfile();
    // Reset form
    newTask.value = { video_type: 'video', video_link: '', title: '', quantity: 100 };
    formError.value = '';
  } catch (e) {
    formError.value = "Failed to create task";
  }
};

const showDetails = (order: any) => {
  selectedOrder.value = order;
  isDetailModalOpen.value = true;
};

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  fetchOrders();
});
</script>

<template>
  <div class="min-h-screen bg-gray-100 font-sans">
    <!-- Header -->
    <header class="bg-white shadow px-6 py-4 flex justify-between items-center">
      <div class="text-xl font-bold text-navy-blue flex items-center gap-4">
          <span>My Dashboard</span>
          <div class="flex gap-2 text-sm">
              <button @click="router.push('/')" class="text-blue-600 hover:underline">Home</button>
              <button @click="router.push('/seo-class')" class="text-blue-600 hover:underline">SEO Class</button>
          </div>
      </div>
      <div class="flex items-center space-x-6">
        <div class="text-gray-700">User: <span class="font-semibold">{{ authStore.user?.username }}</span></div>
        <div class="text-gray-700">Balance: <span class="font-semibold text-green-600">₹{{ authStore.user?.balance }}</span></div>
        <button @click="isRechargeModalOpen = true" class="bg-india-green text-white px-4 py-1 rounded hover:bg-green-700 transition-colors shadow-sm">Recharge</button>
        <button @click="authStore.logout(); router.push('/')" class="text-red-500 hover:text-red-700">Logout</button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Empty State -->
      <div v-if="orders.length === 0" class="flex flex-col items-center justify-center h-96 bg-white rounded-lg shadow">
        <p class="text-gray-500 text-lg mb-4">No tasks found.</p>
        <button @click="openCreateModal" class="flex items-center bg-saffron text-white px-6 py-3 rounded-lg hover:bg-orange-600 transition-colors shadow-md">
          <Plus class="w-5 h-5 mr-2" /> Create New Task
        </button>
      </div>

      <!-- Order List -->
      <div v-else>
        <div class="bg-white rounded-lg shadow overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Task ID</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Link</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quantity</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ order.task_id }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-500 truncate max-w-xs">
                  <a :href="order.video_link" target="_blank">{{ order.video_link }}</a>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.quantity }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span v-if="order.status === 'waiting'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                    Waiting
                  </span>
                  <span v-else-if="order.status === 'in_progress'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                    In Progress
                  </span>
                  <span v-else-if="order.status === 'success'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Success
                  </span>
                  <span v-else class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                    Failed
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button @click="showDetails(order)" class="text-navy-blue hover:text-saffron">Details</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Big Button at Bottom -->
        <div class="mt-8 flex justify-center">
           <button @click="openCreateModal" class="flex items-center bg-saffron text-white px-8 py-4 rounded-lg text-lg hover:bg-orange-600 transition-colors shadow-xl transform hover:scale-105">
             <Plus class="w-6 h-6 mr-2" /> Create New Task
           </button>
        </div>
      </div>
    </main>

    <!-- Create Task Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-lg p-6 animate-fade-in-up">
        <h3 class="text-2xl font-bold mb-4 text-navy-blue">Create New Task</h3>
        <form @submit.prevent="submitTask" class="space-y-4">
          <div>
            <label class="block text-gray-700 mb-1">Video Type</label>
            <div class="flex space-x-4">
              <label class="flex items-center">
                <input type="radio" v-model="newTask.video_type" value="video" class="mr-2 text-saffron focus:ring-saffron"> Video
              </label>
              <label class="flex items-center">
                <input type="radio" v-model="newTask.video_type" value="shorts" class="mr-2 text-saffron focus:ring-saffron"> Shorts
              </label>
            </div>
          </div>
          <div>
            <label class="block text-gray-700 mb-1">Video Link</label>
            <input v-model="newTask.video_link" type="url" class="w-full border p-2 rounded focus:ring-2 focus:ring-saffron outline-none" placeholder="https://youtube.com/..." required>
          </div>
          <div>
            <label class="block text-gray-700 mb-1">Video Title</label>
            <input v-model="newTask.title" type="text" class="w-full border p-2 rounded focus:ring-2 focus:ring-saffron outline-none" required>
          </div>
          <div>
            <label class="block text-gray-700 mb-1">Quantity</label>
            <input v-model.number="newTask.quantity" type="number" min="1" class="w-full border p-2 rounded focus:ring-2 focus:ring-saffron outline-none" required>
            <p class="text-xs text-gray-500 mt-1">Cost: ₹2 per unit</p>
          </div>
          
          <p v-if="formError" class="text-red-500 text-sm">{{ formError }}</p>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="isModalOpen = false" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded">Cancel</button>
            <button type="submit" class="bg-saffron text-white px-6 py-2 rounded hover:bg-orange-600 shadow-md">Submit Task</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Recharge Modal -->
    <div v-if="isRechargeModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
       <div class="bg-white rounded-lg shadow-xl w-full max-w-sm p-6 text-center">
          <h3 class="text-xl font-bold mb-4 text-navy-blue">Recharge Balance</h3>
          <p class="text-gray-600 mb-6">Please contact customer support to recharge your wallet.</p>
          <div class="space-y-3">
             <a href="https://telegram.org" target="_blank" class="block w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Contact via Telegram</a>
             <a href="https://whatsapp.com" target="_blank" class="block w-full bg-green-500 text-white py-2 rounded hover:bg-green-600">Contact via WhatsApp</a>
          </div>
          <button @click="isRechargeModalOpen = false" class="mt-4 text-gray-500 hover:text-gray-700">Close</button>
       </div>
    </div>

    <!-- Detail Modal -->
    <div v-if="isDetailModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
       <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-6">
          <h3 class="text-xl font-bold mb-4 text-navy-blue">Task Details</h3>
          <div v-if="selectedOrder" class="space-y-2">
             <p><strong>ID:</strong> {{ selectedOrder.task_id }}</p>
             <p><strong>Status:</strong> {{ selectedOrder.status }}</p>
             <div v-if="selectedOrder.status === 'failed'" class="bg-red-50 p-3 rounded border border-red-200">
                <p class="text-red-700 font-semibold">Failure Reason:</p>
                <p class="text-red-600">{{ selectedOrder.fail_reason || 'Unknown error' }}</p>
             </div>
             <p v-else class="text-gray-500 italic">No additional details available.</p>
          </div>
          <div class="flex justify-end mt-6">
             <button @click="isDetailModalOpen = false" class="bg-navy-blue text-white px-4 py-2 rounded hover:bg-blue-900">Close</button>
          </div>
       </div>
    </div>

  </div>
</template>
