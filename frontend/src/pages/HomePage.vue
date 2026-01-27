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

const getFullUrl = (url: string) => {
    if (url && url.startsWith('/')) {
         const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
         return `${baseUrl}${url}`;
    }
    return url;
};

// Data-前端图片
const slogan = ref({
  text: "",
  image: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=India%20YouTube%20Growth%20Success%20Digital%20Marketing%20South%20Asian%20Business&image_size=landscape_16_9"
});

const intro = ref({
  text: "We provide authentic engagement to help you grow.",
  flowchart: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=SEO%20Process%20Infographic%20Flowchart%20Step%20by%20Step%20Analysis%20Optimization%20Ranking%20Growth&image_size=landscape_16_9"
});

const cases = ref([
  { id: 1, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Gaming%20Success&image_size=landscape_16_9", text: "Gaming Channel +500% Subs" },
  { id: 2, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Cooking%20Vlog%20Viral&image_size=landscape_16_9", text: "Cooking Vlog 1M Views" },
  { id: 3, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Tech%20Review%20Growth&image_size=landscape_16_9", text: "Tech Reviews Organic Growth" },
  { id: 4, img: "https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=YouTube%20Channel%20Screenshot%20Music%20Video%20Trending&image_size=landscape_16_9", text: "Music Video Trending #1" },
]);
const caseSummary = ref("Our success stories (and more...)");

const faqs = ref([
  { q: "Is this safe?", a: "Yes, we use 100% real interactions." },
  { q: "How fast is delivery?", a: "Starts within 24 hours." },
  { q: "Can I get a refund?", a: "If we fail to deliver, yes." },
]);

onMounted(async () => {
    try {
        const res = await axios.get('/api/home-config/');
        if (res.data && res.data.length > 0) {
            // The API returns an array, but we usually only care about the first active config
            // Since we are creating/editing config, we might have multiple if not handled strictly as singleton
            // Let's take the last one (most recently created) or first one. 
            // AdminPage uses ID, implying one row. 
            
            // Let's assume we want the *latest* config if multiple exist, or just the first.
            // If the Admin page edits a specific ID, we should probably fetch that specific one or just the latest.
            // Given the Admin logic edits `res.data[0]` if exists, let's stick to index 0 but ensure it's not stale.
            
            // Actually, let's look at how AdminPage fetches: `homeRes.data[0]`.
            // If multiple configs are created via POST, we might be seeing an old one here if we pick [0] and it's not ordered by -id.
            // But let's check the fields.
            
            const config = res.data[0]; 
            
            if (config.slogan_text) slogan.value.text = config.slogan_text;
            if (config.slogan_image) slogan.value.image = getFullUrl(config.slogan_image);
            
            if (config.intro_text) intro.value.text = config.intro_text;
            if (config.intro_flowchart) intro.value.flowchart = getFullUrl(config.intro_flowchart);
            
            // Map cases if images exist, otherwise keep default
            if (config.case_1_img) cases.value[0].img = getFullUrl(config.case_1_img);
            if (config.case_2_img) cases.value[1].img = getFullUrl(config.case_2_img);
            if (config.case_3_img) cases.value[2].img = getFullUrl(config.case_3_img);
            if (config.case_4_img) cases.value[3].img = getFullUrl(config.case_4_img);
            
            // Map case text to all cases or a specific area? 
             // The template uses `cases[0].text` for the footer note. 
             // Let's update that footer note text from `case_text`.
             if (config.case_text) {
                 caseSummary.value = config.case_text;
             }
         }
        
        const faqRes = await axios.get('/api/faqs/');
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
      <div class="w-full px-6 py-3 flex justify-between items-center">
        <!-- Logo -->
        <div class="text-2xl font-bold text-saffron tracking-wider font-serif flex-shrink-0">
          AutoLaK <span class="text-navy-blue">SEO</span>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex space-x-6 items-center flex-grow justify-end">
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
      <div v-if="isMenuOpen" class="md:hidden bg-white border-t p-4 space-y-4 absolute top-16 left-0 w-full h-[calc(100vh-4rem)] overflow-y-auto shadow-xl">
         <div class="space-y-2">
            <p class="font-semibold text-gray-500">Navigation</p>
            <a @click="scrollToSection('intro'); isMenuOpen = false" class="block pl-4 py-1 hover:text-saffron cursor-pointer">Introduction</a>
            <a @click="scrollToSection('cases'); isMenuOpen = false" class="block pl-4 py-1 hover:text-saffron cursor-pointer">Success Cases</a>
            <a @click="scrollToSection('faq'); isMenuOpen = false" class="block pl-4 py-1 hover:text-saffron cursor-pointer">FAQ</a>
         </div>
         <div class="space-y-2">
            <p class="font-semibold text-gray-500">About Us</p>
            <a @click="openExternalLink('https://t.me/AutoLakBSOfficial/5'); isMenuOpen = false" class="block pl-4 py-1 hover:text-saffron cursor-pointer">Telegram</a>
            <a @click="openExternalLink('https://wa.me/601169686094'); isMenuOpen = false" class="block pl-4 py-1 hover:text-saffron cursor-pointer">WhatsApp</a>
            <a @click="openExternalLink('https://www.youtube.com/@AyanKhan-g7o1g'); isMenuOpen = false" class="block pl-4 py-1 hover:text-saffron cursor-pointer">YouTube</a>
         </div>
         <button @click="navigateTo('/seo-class'); isMenuOpen = false" class="block w-full text-left py-2 hover:text-saffron">SEO Class</button>
         
         <template v-if="!authStore.isAuthenticated">
            <button @click="navigateTo('/login'); isMenuOpen = false" class="block w-full text-left py-2 hover:text-saffron">Login</button>
            <button @click="navigateTo('/register'); isMenuOpen = false" class="block w-full bg-saffron text-white px-4 py-2 rounded-md text-center">Register</button>
         </template>
         <template v-else>
            <div class="flex items-center space-x-2 py-2 border-t border-gray-100 mt-2 pt-2">
                <img :src="authStore.userAvatar" class="w-8 h-8 rounded-full" />
                <span class="font-bold">{{ authStore.user?.username }}</span>
            </div>
            <button @click="handleLogout(); isMenuOpen = false" class="block w-full text-left py-2 text-red-500">Logout</button>
         </template>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-16">
      <!-- Slogan Section -->
      <section id="slogan" class="relative min-h-[85vh] flex items-center bg-navy-blue overflow-hidden">
        <!-- Decorative Background Elements -->
        <div class="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-white/5 to-transparent skew-x-12 pointer-events-none"></div>
        <div class="absolute bottom-0 left-0 w-1/3 h-1/2 bg-gradient-to-t from-black/20 to-transparent rounded-tr-full pointer-events-none"></div>
        
        <div class="container mx-auto px-6 h-full flex flex-col-reverse md:flex-row items-center relative z-10 py-12 md:py-0">
          <!-- Left: Text Content -->
          <div class="w-full md:w-1/2 text-left text-white z-20 md:pr-12 mt-10 md:mt-0 flex flex-col justify-center">
            <div class="inline-block bg-saffron/20 text-saffron px-4 py-1 rounded-full text-sm font-semibold mb-6 w-fit border border-saffron/30 backdrop-blur-sm">
              🚀 #1 YouTube Growth Service
            </div>
            <h1 class="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight tracking-tight">
              {{ slogan.text }}
            </h1>
            <p class="text-gray-300 text-lg md:text-xl mb-10 max-w-xl leading-relaxed">
              We provide authentic engagement to help you achieve your digital goals. Join thousands of creators growing with AutoLaK.
            </p>
            <div class="flex flex-col sm:flex-row gap-4">
                <button @click="handleGetStarted" class="bg-gradient-to-r from-saffron to-orange-600 text-white text-lg font-bold px-8 py-4 rounded-xl hover:shadow-lg hover:shadow-orange-500/30 transition-all transform hover:-translate-y-1">
                  Get Started Now
                </button>
                <button @click="scrollToSection('intro')" class="bg-white/10 text-white border border-white/20 text-lg font-semibold px-8 py-4 rounded-xl hover:bg-white/20 transition-all">
                  Learn More
                </button>
            </div>
            
            <!-- Stats Row -->
            <div class="mt-12 flex items-center gap-8 border-t border-white/10 pt-8">
                <div>
                    <p class="text-3xl font-bold text-white">10k+</p>
                    <p class="text-gray-400 text-sm">Happy Clients</p>
                </div>
                <div>
                    <p class="text-3xl font-bold text-white">5M+</p>
                    <p class="text-gray-400 text-sm">Views Delivered</p>
                </div>
                <div>
                    <p class="text-3xl font-bold text-white">24/7</p>
                    <p class="text-gray-400 text-sm">Support</p>
                </div>
            </div>
          </div>
          
          <!-- Right: Image (Full Width/Height Style) -->
          <div class="w-full md:w-1/2 h-[400px] md:h-[600px] relative z-10">
             <!-- Abstract Shape Container -->
             <div class="relative w-full h-full">
                 <!-- Main Image with Mask -->
                 <div class="absolute inset-0 md:-right-20 md:-top-10 md:-bottom-10 bg-white/5 rounded-3xl transform rotate-3 backdrop-blur-sm border border-white/10"></div>
                 <div class="absolute inset-0 md:left-4 md:right-4 md:top-4 md:bottom-4 rounded-2xl overflow-hidden shadow-2xl border border-white/10">
                    <img :src="slogan.image" alt="Visual" class="w-full h-full object-cover transform hover:scale-105 transition-transform duration-1000" />
                    <!-- Overlay Gradient -->
                    <div class="absolute inset-0 bg-gradient-to-t from-navy-blue/80 via-transparent to-transparent opacity-60"></div>
                 </div>
                 
                 <!-- Floating Card 1 -->
                 <div class="absolute top-10 -left-6 bg-white/10 backdrop-blur-md border border-white/20 p-4 rounded-xl shadow-xl animate-bounce hidden md:block" style="animation-duration: 3s;">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">✓</div>
                        <div>
                            <p class="text-white font-bold text-sm">Order Completed</p>
                            <p class="text-green-300 text-xs">+500 Subscribers</p>
                        </div>
                    </div>
                 </div>

                 <!-- Floating Card 2 -->
                 <div class="absolute bottom-20 -right-4 bg-white/10 backdrop-blur-md border border-white/20 p-4 rounded-xl shadow-xl animate-bounce hidden md:block" style="animation-duration: 4s; animation-delay: 1s;">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white">
                             <Clock class="w-5 h-5" />
                        </div>
                        <div>
                            <p class="text-white font-bold text-sm">Fast Delivery</p>
                            <p class="text-blue-200 text-xs">Starts in 24h</p>
                        </div>
                    </div>
                 </div>
             </div>
          </div>
        </div>
      </section>

      <!-- Intro Section -->
      <section id="intro" class="py-20 bg-white">
        <div class="container mx-auto px-4">
          <h2 class="text-3xl font-bold text-center mb-12 text-navy-blue">The Complete Guide to YouTube SEO</h2>
          <p class="text-center text-gray-600 max-w-2xl mx-auto mb-10">{{ intro.text }}</p>
          
          <div class="max-w-7xl mx-auto pb-8">
            <div class="grid grid-cols-1 md:grid-cols-5 gap-8 md:gap-4 relative">
                
                <!-- Column 1: Preparation -->
                <div class="flex flex-col gap-4 relative">
                    <div class="bg-blue-50 text-blue-800 font-bold p-3 rounded text-center h-16 flex items-center justify-center border-b-2 border-blue-200">
                        Preparation Phase
                    </div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm relative">
                        <span class="font-bold text-blue-600 mr-2">1.</span>
                        <span class="font-semibold text-gray-800">Keyword Research</span>
                        <ul class="text-xs text-gray-600 mt-2 list-disc list-inside">
                            <li>Discover Trending Topics</li>
                            <li>Analyze Search Intent</li>
                            <li>Use Tools: Google Trends, VidIQ, TubeBuddy</li>
                        </ul>
                    </div>
                    <div class="flex justify-center text-blue-500"><ChevronDown /></div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm relative">
                        <span class="font-bold text-blue-600 mr-2">2.</span>
                        <span class="font-semibold text-gray-800">Content Planning</span>
                        <ul class="text-xs text-gray-600 mt-2 list-disc list-inside">
                            <li>Create High-Retention Script</li>
                            <li>Define Structure & Hook</li>
                        </ul>
                    </div>
                    <!-- Mobile Flow Arrow -->
                    <div class="md:hidden flex justify-center text-blue-300 py-2">
                        <ChevronDown class="w-8 h-8 animate-bounce opacity-50" />
                    </div>
                </div>

                <!-- Column 2: Production -->
                <div class="flex flex-col gap-4 relative">
                    <div class="bg-blue-50 text-blue-800 font-bold p-3 rounded text-center h-16 flex items-center justify-center border-b-2 border-blue-200">
                        Production & File Optimization
                    </div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm">
                        <span class="font-bold text-blue-600 mr-2">3.</span>
                        <span class="font-semibold text-gray-800">High-Quality Video</span>
                        <ul class="text-xs text-gray-600 mt-2 list-disc list-inside">
                            <li>Focus on Visuals & Audio</li>
                            <li>Maintain Audience Engagement</li>
                        </ul>
                    </div>
                    <div class="flex justify-center text-blue-500"><ChevronDown /></div>
                    <div class="border-2 border-orange-300 rounded-lg p-3 bg-orange-50 shadow-sm">
                        <span class="font-bold text-orange-600 mr-2">4.</span>
                        <span class="font-semibold text-gray-800">File Optimization</span>
                        <ul class="text-xs text-gray-600 mt-2 list-disc list-inside">
                            <li>Include Keyword in Filename</li>
                            <li>Use Relevant Metadata</li>
                        </ul>
                    </div>
                    <!-- Mobile Flow Arrow -->
                    <div class="md:hidden flex justify-center text-blue-300 py-2">
                        <ChevronDown class="w-8 h-8 animate-bounce opacity-50" />
                    </div>
                </div>

                <!-- Column 3: Upload -->
                <div class="flex flex-col gap-4 relative">
                    <div class="bg-blue-50 text-blue-800 font-bold p-3 rounded text-center h-16 flex items-center justify-center border-b-2 border-blue-200">
                        Upload & Metadata Optimization
                    </div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm">
                        <span class="font-bold text-blue-600 mr-2">5.</span>
                        <span class="font-semibold text-gray-800">Title Optimization</span>
                        <p class="text-xs text-gray-600 mt-1">Include Primary Keyword, Click-Worthy</p>
                    </div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm">
                        <span class="font-bold text-blue-600 mr-2">6.</span>
                        <span class="font-semibold text-gray-800">Description</span>
                        <p class="text-xs text-gray-600 mt-1">Keywords in First 2-3 Sentences, Call-to-Action</p>
                    </div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm">
                        <span class="font-bold text-blue-600 mr-2">7.</span>
                        <span class="font-semibold text-gray-800">Tags & Categories</span>
                    </div>
                    <div class="border-2 border-green-400 rounded-lg p-3 bg-green-50 shadow-sm">
                        <span class="font-bold text-green-700 mr-2">8.</span>
                        <span class="font-semibold text-gray-800">Thumbnail Design</span>
                        <p class="text-xs text-gray-600 mt-1">High Contrast, Clear Text</p>
                    </div>
                    <div class="border-2 border-green-400 rounded-lg p-3 bg-green-50 shadow-sm">
                        <span class="font-bold text-green-700 mr-2">9.</span>
                        <span class="font-semibold text-gray-800">Cards & End Screens</span>
                    </div>
                    <div class="border-2 border-green-400 rounded-lg p-3 bg-green-50 shadow-sm">
                        <span class="font-bold text-green-700 mr-2">10.</span>
                        <span class="font-semibold text-gray-800">Captions & CC</span>
                    </div>
                    <!-- Mobile Flow Arrow -->
                    <div class="md:hidden flex justify-center text-blue-300 py-2">
                        <ChevronDown class="w-8 h-8 animate-bounce opacity-50" />
                    </div>
                </div>

                <!-- Column 4: Post-Upload -->
                <div class="flex flex-col gap-4 relative">
                    <div class="bg-blue-50 text-blue-800 font-bold p-3 rounded text-center h-16 flex items-center justify-center border-b-2 border-blue-200">
                        Post-Upload & Promotion
                    </div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm">
                        <span class="font-bold text-blue-600 mr-2">11.</span>
                        <span class="font-semibold text-gray-800">Early Engagement</span>
                        <p class="text-xs text-gray-600 mt-1">Reply to Comments, Pin Question</p>
                    </div>
                    <div class="flex justify-center text-blue-500"><ChevronDown /></div>
                    <div class="border-2 border-blue-400 rounded-lg p-3 bg-white shadow-sm">
                        <span class="font-bold text-blue-600 mr-2">12.</span>
                        <span class="font-semibold text-gray-800">Promotion</span>
                        <p class="text-xs text-gray-600 mt-1">Social Media, Email Marketing</p>
                    </div>
                    <div class="flex justify-center text-blue-500"><ChevronDown /></div>
                    <div class="border-2 border-green-400 rounded-lg p-3 bg-green-50 shadow-sm">
                        <span class="font-bold text-green-700 mr-2">13.</span>
                        <span class="font-semibold text-gray-800">Playlist Strategy</span>
                    </div>
                    <!-- Mobile Flow Arrow -->
                    <div class="md:hidden flex justify-center text-blue-300 py-2">
                        <ChevronDown class="w-8 h-8 animate-bounce opacity-50" />
                    </div>
                </div>

                <!-- Column 5: Analysis -->
                <div class="flex flex-col gap-4 relative">
                    <div class="bg-blue-50 text-blue-800 font-bold p-3 rounded text-center h-16 flex items-center justify-center border-b-2 border-blue-200">
                        Analysis & Iteration
                    </div>
                    <div class="border-2 border-green-400 rounded-lg p-3 bg-white shadow-sm">
                        <span class="font-bold text-green-700 mr-2">14.</span>
                        <span class="font-semibold text-gray-800">Performance Tracking</span>
                        <ul class="text-xs text-gray-600 mt-2 list-disc list-inside">
                            <li>YouTube Analytics</li>
                            <li>Key Metrics: CTR, Retention</li>
                        </ul>
                    </div>
                    <div class="flex justify-center text-blue-500"><ChevronDown /></div>
                    <div class="border-2 border-green-400 rounded-lg p-3 bg-green-50 shadow-sm">
                        <span class="font-bold text-green-700 mr-2">15.</span>
                        <span class="font-semibold text-gray-800">Strategy Adjustment</span>
                        <ul class="text-xs text-gray-600 mt-2 list-disc list-inside">
                            <li>Analyze Success/Failure</li>
                            <li>Optimize Future Content</li>
                        </ul>
                    </div>
                </div>

            </div>
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
          <p class="text-center mt-12 text-gray-500 italic">{{ caseSummary }}</p>
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
