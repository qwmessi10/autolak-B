<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Menu, X, ChevronDown, User, LogOut } from 'lucide-vue-next';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const router = useRouter();
const authStore = useAuthStore();
const isMenuOpen = ref(false);
const isNavDropdownOpen = ref(false);
const isAboutDropdownOpen = ref(false);

const scrollToSection = (id: string) => {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
  isNavDropdownOpen.value = false;
};

const navigateTo = (path: string) => {
  router.push(path);
};

const handleGetStarted = () => {
  if (authStore.isAuthenticated) {
    if (authStore.isAdmin) {
       navigateTo('/admin');
    } else {
       navigateTo('/order');
    }
  } else {
    navigateTo('/register');
  }
};

const handleLogout = () => {
    authStore.logout();
    navigateTo('/login');
};

const openExternalLink = (url: string) => {
    window.open(url, '_blank');
};

// Data
const slogan = ref({
  text: "Boost Your YouTube Channel with AutoLaK",
  image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=India%20YouTube%20Growth%20Success%20Digital%20Marketing%20South%20Asian%20Business&image_size=landscape_16_9"
});

const intro = ref({
  text: "We provide authentic engagement to help you grow.",
  flowchart: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Process%20Flowchart%20Infographic%20Business%20Steps%20Clean%20Design&image_size=landscape_16_9"
});

const cases = ref([
  { id: 1, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Gaming%20Success&image_size=landscape_16_9", text: "Gaming Channel +500% Subs" },
  { id: 2, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Cooking%20Vlog%20Viral&image_size=landscape_16_9", text: "Cooking Vlog 1M Views" },
  { id: 3, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Tech%20Review%20Growth&image_size=landscape_16_9", text: "Tech Reviews Organic Growth" },
  { id: 4, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Music%20Video%20Trending&image_size=landscape_16_9", text: "Music Video Trending #1" },
]);

const faqs = ref([
  { q: "Is this safe?", a: "Yes, we use 100% real interactions." },
  { q: "How fast is delivery?", a: "Starts within 24 hours." },
  { q: "Can I get a refund?", a: "If we fail to deliver, yes." },
]);

onMounted(async () => {
    try {
        const res = await axios.get('http://localhost:8000/api/home-config/');
        if (res.data && res.data.length > 0) {
            const config = res.data[0];
            slogan.value.text = config.slogan_text || slogan.value.text;
            if (config.slogan_image) slogan.value.image = config.slogan_image;
            
            intro.value.text = config.intro_text || intro.value.text;
            if (config.intro_flowchart) intro.value.flowchart = config.intro_flowchart;
            
            // Map cases if images exist, otherwise keep default
            if (config.case_1_img) cases.value[0].img = config.case_1_img;
            if (config.case_2_img) cases.value[1].img = config.case_2_img;
            if (config.case_3_img) cases.value[2].img = config.case_3_img;
            if (config.case_4_img) cases.value[3].img = config.case_4_img;
            // Note: DB model has single case_text, assuming shared or ignored for now
        }
        
        const faqRes = await axios.get('http://localhost:8000/api/faqs/');
        if (faqRes.data && faqRes.data.length > 0) {
            faqs.value = faqRes.data.map((f: any) => ({ q: f.question, a: f.answer }));
        }
    } catch (e) {
        console.error("Failed to fetch home config", e);
    }
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
    <!-- Navigation -->
    <nav class="fixed top-0 w-full bg-white shadow-md z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <!-- Logo -->
        <div class="text-2xl font-bold text-saffron tracking-wider font-serif">
          AutoLaK <span class="text-navy-blue">SEO</span>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex space-x-6 items-center">
          <div class="relative group">
            <button class="flex items-center hover:text-saffron transition-colors py-2">
              Navigation <ChevronDown class="w-4 h-4 ml-1" />
            </button>
            <!-- Dropdown -->
            <div class="absolute left-0 mt-0 w-48 bg-white shadow-lg rounded-md hidden group-hover:block border-t-2 border-saffron">
              <a @click="scrollToSection('intro')" class="block px-4 py-2 hover:bg-orange-50 cursor-pointer">Introduction</a>
              <a @click="scrollToSection('cases')" class="block px-4 py-2 hover:bg-orange-50 cursor-pointer">Success Cases</a>
              <a @click="scrollToSection('faq')" class="block px-4 py-2 hover:bg-orange-50 cursor-pointer">FAQ</a>
            </div>
          </div>
          
          <!-- About Us Dropdown -->
          <div class="relative group">
            <button class="flex items-center hover:text-saffron transition-colors py-2">
              About Us <ChevronDown class="w-4 h-4 ml-1" />
            </button>
            <div class="absolute left-0 mt-0 w-48 bg-white shadow-lg rounded-md hidden group-hover:block border-t-2 border-saffron">
              <a @click="openExternalLink('https://t.me/AutoLakBSOfficial/5')" class="block px-4 py-2 hover:bg-orange-50 cursor-pointer">Telegram</a>
              <a @click="openExternalLink('https://wa.me/601169686094')" class="block px-4 py-2 hover:bg-orange-50 cursor-pointer">WhatsApp</a>
              <a @click="openExternalLink('https://www.youtube.com/@AyanKhan-g7o1g')" class="block px-4 py-2 hover:bg-orange-50 cursor-pointer">YouTube</a>
            </div>
          </div>

          <!-- SEO Class -->
          <button @click="navigateTo('/seo-class')" class="hover:text-saffron transition-colors">SEO Class</button>

          <template v-if="!authStore.isAuthenticated">
             <button @click="navigateTo('/login')" class="hover:text-saffron transition-colors">Login</button>
             <button @click="navigateTo('/register')" class="bg-saffron text-white px-4 py-2 rounded-md hover:bg-orange-600 transition-colors shadow-md">Free Trial / Register</button>
          </template>
          <template v-else>
             <div class="flex items-center space-x-3">
                <img :src="authStore.userAvatar" alt="Avatar" class="w-8 h-8 rounded-full border border-gray-200" />
                <span class="font-semibold text-navy-blue">{{ authStore.user?.username }}</span>
                <button @click="handleLogout" class="text-gray-500 hover:text-red-500" title="Logout">
                    <LogOut class="w-5 h-5" />
                </button>
             </div>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <button @click="isMenuOpen = !isMenuOpen" class="md:hidden">
          <Menu v-if="!isMenuOpen" />
          <X v-else />
        </button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="isMenuOpen" class="md:hidden bg-white border-t p-4 space-y-4">
         <div class="space-y-2">
            <p class="font-semibold text-gray-500">Navigation</p>
            <a @click="scrollToSection('intro')" class="block pl-4 py-1 hover:text-saffron">Introduction</a>
            <a @click="scrollToSection('cases')" class="block pl-4 py-1 hover:text-saffron">Success Cases</a>
            <a @click="scrollToSection('faq')" class="block pl-4 py-1 hover:text-saffron">FAQ</a>
         </div>
         <div class="space-y-2">
            <p class="font-semibold text-gray-500">About Us</p>
            <a @click="openExternalLink('https://t.me/AutoLakBSOfficial/5')" class="block pl-4 py-1 hover:text-saffron">Telegram</a>
            <a @click="openExternalLink('https://wa.me/601169686094')" class="block pl-4 py-1 hover:text-saffron">WhatsApp</a>
            <a @click="openExternalLink('https://www.youtube.com/@AyanKhan-g7o1g')" class="block pl-4 py-1 hover:text-saffron">YouTube</a>
         </div>
         <button @click="navigateTo('/seo-class')" class="block w-full text-left py-2 hover:text-saffron">SEO Class</button>
         
         <template v-if="!authStore.isAuthenticated">
            <button @click="navigateTo('/login')" class="block w-full text-left py-2 hover:text-saffron">Login</button>
            <button @click="navigateTo('/register')" class="block w-full bg-saffron text-white px-4 py-2 rounded-md text-center">Register</button>
         </template>
         <template v-else>
            <div class="flex items-center space-x-2 py-2 border-t border-gray-100 mt-2 pt-2">
                <img :src="authStore.userAvatar" class="w-8 h-8 rounded-full" />
                <span class="font-bold">{{ authStore.user?.username }}</span>
            </div>
            <button @click="handleLogout" class="block w-full text-left py-2 text-red-500">Logout</button>
         </template>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-16">
      <!-- Slogan Section -->
      <section id="slogan" class="relative h-[80vh] flex items-center justify-center overflow-hidden">
        <img :src="slogan.image" alt="Background" class="absolute inset-0 w-full h-full object-cover opacity-90" />
        <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
        <div class="relative z-10 text-center px-4 max-w-4xl">
          <h1 class="text-4xl md:text-6xl font-bold text-white mb-6 drop-shadow-lg">{{ slogan.text }}</h1>
          <button @click="handleGetStarted" class="bg-india-green text-white text-xl px-8 py-3 rounded-full hover:bg-green-700 transition-transform hover:scale-105 shadow-xl animate-bounce">
            Get Started Now
          </button>
        </div>
      </section>

      <!-- Intro Section -->
      <section id="intro" class="py-20 bg-white">
        <div class="container mx-auto px-4">
          <h2 class="text-3xl font-bold text-center mb-12 text-navy-blue">How We Work</h2>
          <p class="text-center text-gray-600 max-w-2xl mx-auto mb-10">{{ intro.text }}</p>
          <div class="w-full max-w-5xl mx-auto border-4 border-gray-100 rounded-xl overflow-hidden shadow-lg">
             <img :src="intro.flowchart" alt="Process Flow" class="w-full" />
          </div>
        </div>
      </section>

      <!-- Success Cases -->
      <section id="cases" class="py-20 bg-gradient-to-b from-orange-50 to-white">
        <div class="container mx-auto px-4">
          <h2 class="text-3xl font-bold text-center mb-12 text-navy-blue">Success Stories</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            <div v-for="item in cases" :key="item.id" class="group relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300">
              <div class="aspect-video relative overflow-hidden">
                <img :src="item.img" :alt="item.text" class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500" />
                <!-- Gradient Overlay -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-90"></div>
                <div class="absolute bottom-0 left-0 p-6">
                  <p class="text-white font-semibold text-lg">{{ item.text }}</p>
                </div>
              </div>
            </div>
          </div>
          <p class="text-center mt-12 text-gray-500 italic">{{ cases[0].text }} (and more...)</p>
        </div>
      </section>

      <!-- FAQ Section -->
      <section id="faq" class="py-20 bg-navy-blue text-white">
        <div class="container mx-auto px-4">
          <h2 class="text-3xl font-bold text-center mb-12 font-serif">Common Questions</h2>
          <div class="max-w-3xl mx-auto space-y-6">
            <div v-for="(item, index) in faqs" :key="index" class="bg-white/10 backdrop-blur-sm rounded-lg p-6 hover:bg-white/20 transition-colors">
              <h3 class="text-xl font-semibold mb-2 text-saffron font-serif">{{ item.q }}</h3>
              <p class="text-gray-200">{{ item.a }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="bg-gray-900 text-gray-400 py-8 text-center">
      <p>&copy; 2024 GlobalViews-Autolak. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
/* Custom fonts or specific tweaks */
</style>
