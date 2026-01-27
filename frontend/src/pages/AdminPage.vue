<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import { X } from 'lucide-vue-next';
import axios from 'axios';
import { marked } from 'marked';

const authStore = useAuthStore();
const router = useRouter();
const activeTab = ref('config'); // config, system, users, seo-class

const users = ref<any[]>([]);
const selectedUser = ref<any>(null);
const userTasks = ref<any[]>([]);
const isUserModalOpen = ref(false);

const failReason = ref('');
const taskToFail = ref<any>(null);

// Config State
const homeConfig = ref<any>({
    slogan_text: '',
    intro_text: '',
    case_text: ''
});
const faqs = ref<any[]>([]);
const systemConfig = ref<any>({
    telegram_bot_token: '',
    telegram_chat_id: ''
});

// SEO Class State
const seoArticles = ref<any[]>([]);
const isArticleModalOpen = ref(false);
const currentArticle = ref<any>({ title: '', content: '' });

// --- Fetch Data ---
const fetchUsers = async () => {
  try {
      const authStore = useAuthStore();
      const config = {
          headers: {
              'Authorization': `Token ${authStore.token}`
          }
      };
      console.log("Requesting users with token:", authStore.token);
      const response = await axios.get('/api/users/admin/users/', config);
      console.log('Fetched users:', response.data);
      users.value = response.data;
  } catch (e: any) {
      console.error("Failed to fetch users", e.response?.data || e);
      if (e.response?.status === 403) {
          alert("Permission denied. Are you sure you are an admin?");
      }
  }
};

const fetchConfig = async () => {
    try {
        // Home Config
        const homeRes = await axios.get('/api/home-config/');
        if (homeRes.data.length > 0) {
            homeConfig.value = homeRes.data[0];
        }
        // FAQs
        const faqRes = await axios.get('/api/faqs/');
        faqs.value = faqRes.data;
        
        // System Config
        const sysRes = await axios.get('/api/admin/system-config/');
        if (sysRes.data.length > 0) {
            systemConfig.value = sysRes.data[0];
        }
        
        // SEO Articles
        const seoRes = await axios.get('/api/admin/seo-articles/');
        seoArticles.value = seoRes.data;
    } catch (e) {
        console.error("Failed to fetch configs", e);
    }
};

// --- User Management ---
const openUserModal = async (user: any) => {
  selectedUser.value = { ...user };
  try {
      const authStore = useAuthStore();
      const config = {
          headers: {
              'Authorization': `Token ${authStore.token}`
          }
      };
      // Correct endpoint for fetching admin orders: /api/admin/orders/
      // The router maps 'admin/orders' under 'api/', so it becomes /api/admin/orders/
      const response = await axios.get('/api/admin/orders/', config); 
      userTasks.value = response.data.filter((o: any) => o.user === user.id);
      isUserModalOpen.value = true;
  } catch (e) {
      console.error("Failed to fetch tasks", e);
      alert("Failed to load user tasks. Please check console for details.");
  }
};

const updateUser = async () => {
    try {
        const authStore = useAuthStore();
        const config = {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        };
        await axios.patch(`/api/users/admin/users/${selectedUser.value.id}/`, {
            balance: selectedUser.value.balance
        }, config);
        isUserModalOpen.value = false;
        fetchUsers();
    } catch (e) {
        alert('Failed to update user');
    }
};

const updateTaskStatus = async (task: any, status: string) => {
    if (status === 'failed') {
        taskToFail.value = task;
        // Prompt for reason? UI simplified: use a separate small modal or prompt
        const reason = prompt("Enter failure reason:");
        if (reason) {
             await performUpdateStatus(task, status, reason);
        }
    } else {
        await performUpdateStatus(task, status);
    }
};

const performUpdateStatus = async (task: any, status: string, reason: string = '') => {
    try {
        const authStore = useAuthStore();
        const config = {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        };
        // Update endpoint to /api/admin/orders/
        await axios.patch(`/api/admin/orders/${task.id}/`, {
            status: status,
            fail_reason: reason
        }, config);
        const t = userTasks.value.find(t => t.id === task.id);
        if (t) {
            t.status = status;
            t.fail_reason = reason;
        }
    } catch (e) {
        alert('Failed to update status');
    }
};

// --- Config Management ---
const saveHomeConfig = async () => {
    try {
        const authStore = useAuthStore();
        // Remove 'Content-Type' header to let browser set it with boundary
        // BUT for simple JSON data, we should use application/json.
        // The issue is mixing multipart/form-data logic with JSON logic.
        // If we are just sending text, we should send JSON.
        
        // Ensure we are sending a clean object
        const payload = {
            slogan_text: homeConfig.value.slogan_text,
            intro_text: homeConfig.value.intro_text,
            case_text: homeConfig.value.case_text
        };

        const config = {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        };
        
        if (homeConfig.value.id) {
            await axios.patch(`/api/admin/home-config/${homeConfig.value.id}/`, payload, config);
        } else {
            await axios.post('/api/admin/home-config/', payload, config);
        }
        alert("Homepage config saved!");
    } catch (e) {
        console.error("Error saving home config", e);
        alert("Error saving home config");
    }
};

const saveSystemConfig = async () => {
    try {
        const authStore = useAuthStore();
        const config = {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        };
        if (systemConfig.value.id) {
            await axios.patch(`/api/admin/system-config/${systemConfig.value.id}/`, systemConfig.value, config);
        } else {
            const res = await axios.post('/api/admin/system-config/', systemConfig.value, config);
            systemConfig.value = res.data; // update with ID
        }
        alert("System config saved!");
    } catch (e) {
        alert("Error saving system config");
    }
};

// FAQ Management
const addFAQ = async () => {
    const q = prompt("Question:");
    const a = prompt("Answer:");
    if (q && a) {
        try {
            const authStore = useAuthStore();
            const config = {
                headers: {
                    'Authorization': `Token ${authStore.token}`
                }
            };
            await axios.post('/api/admin/faqs/', { question: q, answer: a }, config);
            fetchConfig(); // refresh
        } catch(e) { alert("Failed to add FAQ"); }
    }
};

const deleteFAQ = async (id: number) => {
    if (!confirm("Delete this FAQ?")) return;
    try {
        const config = { headers: { 'Authorization': `Token ${authStore.token}` } };
        await axios.delete(`/api/admin/faqs/${id}/`, config);
        const faqRes = await axios.get('/api/admin/faqs/', config);
        faqs.value = faqRes.data;
    } catch (e) { alert("Failed to delete FAQ"); }
};

// --- SEO Class Management ---
const openArticleModal = (article: any = null) => {
    if (article) {
        currentArticle.value = { ...article };
    } else {
        currentArticle.value = { title: '', content: '' };
    }
    isArticleModalOpen.value = true;
};

const insertImageToArticle = () => {
    const url = prompt("Enter image URL:");
    if (url) {
        const imageMarkdown = `![Image Alt](${url})`;
        currentArticle.value.content = (currentArticle.value.content || '') + '\n' + imageMarkdown;
    }
};

const handlePaste = async (event: ClipboardEvent) => {
    const items = event.clipboardData?.items;
    if (!items) return;

    for (const item of items) {
        if (item.type.indexOf('image') !== -1) {
            event.preventDefault();
            const file = item.getAsFile();
            if (!file) continue;

            // Upload image
            const formData = new FormData();
            formData.append('image', file);

            try {
                const authStore = useAuthStore();
                const config = {
                    headers: {
                        'Authorization': `Token ${authStore.token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                };
                const response = await axios.post('/api/upload-image/', formData, config);
                const imageUrl = response.data.url;
                
                // Insert markdown at cursor
                const markdown = `![Image](${imageUrl})`;
                const textarea = event.target as HTMLTextAreaElement;
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                
                currentArticle.value.content = 
                    currentArticle.value.content.substring(0, start) + 
                    markdown + 
                    currentArticle.value.content.substring(end);
                
                // Wait for Vue update then fix cursor position (optional but nice)
            } catch (e) {
                console.error("Failed to upload pasted image", e);
                alert("Failed to upload pasted image.");
            }
        }
    }
};

const saveArticle = async () => {
    try {
        const authStore = useAuthStore();
        const config = {
            headers: {
                'Authorization': `Token ${authStore.token}`
            }
        };
        if (currentArticle.value.id) {
            await axios.patch(`/api/admin/seo-articles/${currentArticle.value.id}/`, currentArticle.value, config);
        } else {
            await axios.post('/api/admin/seo-articles/', currentArticle.value, config);
        }
        isArticleModalOpen.value = false;
        fetchConfig();
    } catch (e) {
        alert("Failed to save article");
    }
};

const deleteArticle = async (id: number) => {
    if (confirm("Delete this article?")) {
        try {
            const authStore = useAuthStore();
            const config = {
                headers: {
                    'Authorization': `Token ${authStore.token}`
                }
            };
            await axios.delete(`/api/admin/seo-articles/${id}/`, config);
            fetchConfig();
        } catch(e) { alert("Failed to delete article"); }
    }
};



onMounted(() => {
  if (!authStore.isAdmin) {
    router.push('/login');
    return;
  }
  fetchUsers();
  fetchConfig();
});
</script>

<template>
  <div class="min-h-screen bg-gray-100 font-sans">
    <header class="bg-navy-blue text-white shadow px-6 py-4 flex justify-between items-center">
      <div class="text-xl font-bold">Admin Dashboard</div>
      <button @click="router.push('/')" class="hover:text-saffron">Back to Site</button>
    </header>

    <div class="container mx-auto px-4 py-8">
      <!-- Tabs -->
      <div class="flex space-x-4 border-b border-gray-300 mb-6">
        <button @click="activeTab = 'config'" :class="{'border-b-2 border-saffron text-saffron font-bold': activeTab === 'config'}" class="px-4 py-2">Site Content</button>
        <button @click="activeTab = 'system'" :class="{'border-b-2 border-saffron text-saffron font-bold': activeTab === 'system'}" class="px-4 py-2">System Config</button>
        <button @click="activeTab = 'seo-class'" :class="{'border-b-2 border-saffron text-saffron font-bold': activeTab === 'seo-class'}" class="px-4 py-2">SEO Class</button>
        <button @click="activeTab = 'users'" :class="{'border-b-2 border-saffron text-saffron font-bold': activeTab === 'users'}" class="px-4 py-2">User Management</button>
      </div>

      <!-- SEO Class Tab -->
      <div v-if="activeTab === 'seo-class'" class="bg-white p-6 rounded shadow">
          <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl font-bold">SEO Articles</h3>
              <button @click="openArticleModal()" class="bg-green-600 text-white px-4 py-2 rounded">+ New Article</button>
          </div>
          
          <div class="space-y-4">
              <div v-for="article in seoArticles" :key="article.id" class="border p-4 rounded hover:bg-gray-50 flex justify-between">
                  <div>
                      <h4 class="font-bold text-lg">{{ article.title }}</h4>
                      <p class="text-gray-500 text-sm">{{ new Date(article.created_at).toLocaleDateString() }}</p>
                  </div>
                  <div class="space-x-2">
                      <button @click="openArticleModal(article)" class="text-blue-600 hover:text-blue-800">Edit</button>
                      <button @click="deleteArticle(article.id)" class="text-red-600 hover:text-red-800">Delete</button>
                  </div>
              </div>
          </div>
      </div>

      <!-- Content Config Tab -->
      <div v-if="activeTab === 'config'" class="bg-white p-6 rounded shadow space-y-8">
        <!-- Main Texts -->
        <div>
            <h3 class="text-xl font-bold mb-4 border-b pb-2">Main Content</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-gray-700 font-semibold">Slogan Text</label>
                    <input v-model="homeConfig.slogan_text" class="w-full border p-2 rounded" />
                </div>
                <div>
                    <label class="block text-gray-700 font-semibold">Intro Text</label>
                    <textarea v-model="homeConfig.intro_text" class="w-full border p-2 rounded" rows="3"></textarea>
                </div>
                <div class="col-span-2">
                     <label class="block text-gray-700 font-semibold">Cases Section Text</label>
                     <textarea v-model="homeConfig.case_text" class="w-full border p-2 rounded" rows="2"></textarea>
                </div>
            </div>
            <button @click="saveHomeConfig" class="mt-4 bg-saffron text-white px-6 py-2 rounded shadow hover:bg-orange-600">Save Content</button>
        </div>

        <!-- FAQs -->
        <div>
            <div class="flex justify-between items-center mb-4 border-b pb-2">
                <h3 class="text-xl font-bold">FAQs</h3>
                <button @click="addFAQ" class="bg-green-600 text-white px-3 py-1 rounded text-sm">+ Add FAQ</button>
            </div>
            <div class="space-y-2">
                <div v-for="faq in faqs" :key="faq.id" class="flex justify-between items-center bg-gray-50 p-3 rounded">
                    <div>
                        <p class="font-bold">{{ faq.question }}</p>
                        <p class="text-gray-600 text-sm">{{ faq.answer }}</p>
                    </div>
                    <button @click="deleteFAQ(faq.id)" class="text-red-500 hover:text-red-700">Delete</button>
                </div>
            </div>
        </div>
      </div>

      <!-- System Config Tab -->
      <div v-if="activeTab === 'system'" class="bg-white p-6 rounded shadow max-w-2xl">
        <h3 class="text-xl font-bold mb-4">Telegram Integration</h3>
        <div class="space-y-4">
            <div>
                <label class="block text-gray-700 font-semibold">Bot Token</label>
                <input v-model="systemConfig.telegram_bot_token" type="password" class="w-full border p-2 rounded" placeholder="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" />
                <p class="text-xs text-gray-500 mt-1">From @BotFather</p>
            </div>
            <div>
                <label class="block text-gray-700 font-semibold">Group Chat ID</label>
                <input v-model="systemConfig.telegram_chat_id" class="w-full border p-2 rounded" placeholder="-1001234567890" />
                <p class="text-xs text-gray-500 mt-1">The ID of the group where orders should be sent.</p>
            </div>
            <button @click="saveSystemConfig" class="bg-blue-600 text-white px-6 py-2 rounded shadow hover:bg-blue-700">Save System Config</button>
        </div>
      </div>

      <!-- Users Tab -->
      <div v-if="activeTab === 'users'" class="bg-white rounded shadow overflow-hidden">
         <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Username</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Balance</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4">{{ user.username }}</td>
                    <td class="px-6 py-4">{{ user.email }}</td>
                    <td class="px-6 py-4">₹{{ user.balance }}</td>
                    <td class="px-6 py-4">
                        <button @click="openUserModal(user)" class="text-blue-600 hover:text-blue-800 font-medium">Manage Tasks</button>
                    </td>
                </tr>
            </tbody>
         </table>
      </div>
    </div>

    <!-- User Modal -->
    <div v-if="isUserModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl p-6 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold">Manage User: {{ selectedUser.username }}</h3>
                <button @click="isUserModalOpen = false" class="text-gray-500 hover:text-gray-700"><X class="w-6 h-6"/></button>
            </div>
            
            <div class="mb-6 border-b pb-6 bg-gray-50 p-4 rounded">
                <h4 class="font-semibold mb-2">💰 Update Balance</h4>
                <div class="flex space-x-2 items-center">
                    <span class="text-lg font-bold">₹</span>
                    <input v-model.number="selectedUser.balance" type="number" class="border p-2 rounded w-32" />
                    <button @click="updateUser" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Update</button>
                </div>
            </div>

            <div>
                <h4 class="font-semibold mb-2">📋 User Tasks</h4>
                <table class="min-w-full divide-y divide-gray-200 border">
                    <thead class="bg-gray-100">
                        <tr>
                            <th class="px-4 py-2 text-left text-xs text-gray-500">ID</th>
                            <th class="px-4 py-2 text-left text-xs text-gray-500">Type</th>
                            <th class="px-4 py-2 text-left text-xs text-gray-500">Link</th>
                            <th class="px-4 py-2 text-left text-xs text-gray-500">Status</th>
                            <th class="px-4 py-2 text-left text-xs text-gray-500">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr v-for="task in userTasks" :key="task.id">
                            <td class="px-4 py-2 text-xs text-gray-500">{{ task.task_id }}</td>
                            <td class="px-4 py-2 text-sm">{{ task.video_type }}</td>
                            <td class="px-4 py-2 text-xs truncate max-w-[150px]"><a :href="task.video_link" target="_blank" class="text-blue-500 hover:underline">{{ task.video_link }}</a></td>
                            <td class="px-4 py-2">
                                <span :class="{
                                    'text-yellow-600 bg-yellow-100 px-2 py-1 rounded text-xs': task.status === 'waiting',
                                    'text-blue-600 bg-blue-100 px-2 py-1 rounded text-xs': task.status === 'in_progress',
                                    'text-green-600 bg-green-100 px-2 py-1 rounded text-xs': task.status === 'success',
                                    'text-red-600 bg-red-100 px-2 py-1 rounded text-xs': task.status === 'failed'
                                }">{{ task.status }}</span>
                                <div v-if="task.fail_reason" class="text-xs text-red-500 mt-1">Reason: {{ task.fail_reason }}</div>
                            </td>
                            <td class="px-4 py-2 flex flex-col space-y-1">
                                <button @click="updateTaskStatus(task, 'in_progress')" class="text-xs border border-blue-500 text-blue-500 hover:bg-blue-50 px-2 py-1 rounded">Start</button>
                                <button @click="updateTaskStatus(task, 'success')" class="text-xs border border-green-500 text-green-500 hover:bg-green-50 px-2 py-1 rounded">Complete</button>
                                <button @click="updateTaskStatus(task, 'failed')" class="text-xs border border-red-500 text-red-500 hover:bg-red-50 px-2 py-1 rounded">Fail</button>
                            </td>
                        </tr>
                        <tr v-if="userTasks.length === 0">
                            <td colspan="5" class="text-center py-4 text-gray-500">No tasks found for this user.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <!-- Article Modal -->
    <div v-if="isArticleModalOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl p-6 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl font-bold">{{ currentArticle.id ? 'Edit' : 'New' }} SEO Article</h3>
                <button @click="isArticleModalOpen = false" class="text-gray-500 hover:text-gray-700"><X class="w-6 h-6"/></button>
            </div>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-gray-700 font-semibold">Title</label>
                    <input v-model="currentArticle.title" class="w-full border p-2 rounded" />
                </div>
                <div>
                    <label class="block text-gray-700 font-semibold mb-2">Content (Markdown Supported)</label>
                    <div class="flex gap-2 mb-2">
                        <button @click="insertImageToArticle" class="bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded text-sm flex items-center">
                            🖼️ Insert Image URL
                        </button>
                    </div>
                    <textarea 
                        v-model="currentArticle.content" 
                        @paste="handlePaste"
                        class="w-full border p-2 rounded h-64 font-mono" 
                        placeholder="# Heading\n\nWrite your article content here... Paste images directly!"></textarea>
                </div>
            </div>

            <div class="mt-6 flex justify-end space-x-3">
                <button @click="isArticleModalOpen = false" class="bg-gray-300 text-gray-700 px-4 py-2 rounded">Cancel</button>
                <button @click="saveArticle" class="bg-saffron text-white px-6 py-2 rounded shadow">Save</button>
            </div>
        </div>
    </div>
  </div>
</template>
