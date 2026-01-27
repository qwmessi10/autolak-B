<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft, BookOpen, Clock, Calendar } from 'lucide-vue-next';
import axios from 'axios';
import { marked } from 'marked';

const router = useRouter();
const articles = ref<any[]>([]);
const selectedArticle = ref<any>(null);

onMounted(async () => {
    try {
        const response = await axios.get('/api/seo-articles/');
        articles.value = response.data;
    } catch (e) {
        console.error("Failed to fetch articles", e);
    }
});

const renderMarkdown = (content: string) => {
    return marked(content);
};

const openArticle = (article: any) => {
    selectedArticle.value = article;
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

const closeArticle = () => {
    selectedArticle.value = null;
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

const getCoverImage = (article: any) => {
    if (article.cover_image) {
        if (article.cover_image.startsWith('/')) {
            return `http://localhost:8000${article.cover_image}`;
        }
        return article.cover_image;
    }
    const prompt = encodeURIComponent(`Abstract SEO Concept ${article.title ? article.title.substring(0, 20) : 'SEO'}`);
    return `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${prompt}&image_size=landscape_16_9`;
};
</script>

<template>
    <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
        <!-- Header -->
        <header class="bg-white shadow-md sticky top-0 z-50">
            <div class="container mx-auto px-6 py-4 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <button @click="selectedArticle ? closeArticle() : router.push('/')" class="text-gray-600 hover:text-saffron transition-colors flex items-center group">
                        <ArrowLeft class="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" />
                        <span class="font-medium">{{ selectedArticle ? 'Back to List' : 'Back to Home' }}</span>
                    </button>
                </div>
                <h1 class="text-xl font-bold text-navy-blue font-serif hidden md:block">SEO Masterclass Forum</h1>
            </div>
        </header>

        <!-- Background Decor -->
        <div class="fixed inset-0 z-0 pointer-events-none opacity-5">
            <div class="absolute top-0 left-0 w-full h-64 bg-gradient-to-b from-navy-blue to-transparent"></div>
        </div>

        <!-- Main Content -->
        <main class="container mx-auto px-4 py-8 relative z-10 min-h-[80vh]">
            
            <!-- Article List View -->
            <div v-if="!selectedArticle">
                <div class="text-center mb-12">
                    <h2 class="text-4xl font-bold text-navy-blue mb-4">Latest Discussions & Guides</h2>
                    <p class="text-gray-600 max-w-2xl mx-auto">Explore our curated collection of SEO strategies, YouTube growth hacks, and digital marketing insights.</p>
                </div>

                <div v-if="articles.length === 0" class="text-center py-20 text-gray-500 bg-white rounded-xl shadow-sm border border-gray-100">
                    <BookOpen class="w-16 h-16 mx-auto mb-4 text-gray-300" />
                    <p class="text-xl font-medium">No articles available yet.</p>
                    <p class="text-sm">Check back soon for new content!</p>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <div v-for="article in articles" :key="article.id" 
                         @click="openArticle(article)"
                         class="bg-white rounded-xl shadow-sm hover:shadow-xl border border-gray-100 transition-all duration-300 cursor-pointer overflow-hidden group flex flex-col h-full">
                        
                        <!-- Thumbnail -->
                        <div class="h-48 bg-gray-100 flex items-center justify-center relative overflow-hidden group-hover:opacity-90 transition-opacity">
                            <img :src="getCoverImage(article)" class="w-full h-full object-cover" loading="lazy" />
                        </div>

                        <div class="p-6 flex-grow flex flex-col">
                            <div class="flex items-center text-xs text-gray-500 mb-3 space-x-4">
                                <span class="flex items-center"><Calendar class="w-3 h-3 mr-1" /> {{ new Date(article.created_at).toLocaleDateString() }}</span>
                                <span class="flex items-center"><Clock class="w-3 h-3 mr-1" /> 5 min read</span>
                            </div>
                            <h3 class="text-xl font-bold text-navy-blue mb-3 group-hover:text-saffron transition-colors line-clamp-2">{{ article.title }}</h3>
                            <p class="text-gray-600 text-sm line-clamp-3 mb-4 flex-grow">
                                {{ article.content.substring(0, 150).replace(/[#*`]/g, '') }}...
                            </p>
                            <div class="mt-auto pt-4 border-t border-gray-50 flex justify-between items-center">
                                <span class="text-saffron font-semibold text-sm group-hover:translate-x-1 transition-transform inline-flex items-center">
                                    Read Article <ArrowLeft class="w-3 h-3 ml-1 rotate-180" />
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Single Article View -->
            <div v-else class="max-w-4xl mx-auto animate-fade-in-up">
                <article class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
                    <!-- Article Header -->
                    <div class="bg-gray-50 p-8 border-b border-gray-100">
                        <div class="flex items-center space-x-2 text-sm text-gray-500 mb-4">
                            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">SEO Guide</span>
                            <span>•</span>
                            <span>{{ new Date(selectedArticle.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) }}</span>
                        </div>
                        <h1 class="text-3xl md:text-4xl font-bold text-navy-blue leading-tight mb-4">{{ selectedArticle.title }}</h1>
                    </div>

                    <!-- Article Body -->
                    <div class="p-8 md:p-12">
                        <div class="prose prose-lg prose-indigo max-w-none text-gray-700 leading-relaxed" v-html="renderMarkdown(selectedArticle.content)"></div>
                    </div>
                    
                    <!-- Article Footer -->
                    <div class="bg-gray-50 p-8 border-t border-gray-100 text-center">
                        <p class="text-gray-600 mb-4">Did you find this helpful?</p>
                        <button @click="closeArticle" class="bg-white border border-gray-300 text-gray-700 px-6 py-2 rounded-full hover:bg-gray-100 transition-colors shadow-sm font-medium">
                            Back to All Articles
                        </button>
                    </div>
                </article>
            </div>

        </main>
    </div>
</template>

<style>
/* Simple Prose styles for Markdown content */
.prose h1 { @apply text-2xl font-bold mt-6 mb-4; }
.prose h2 { @apply text-xl font-bold mt-5 mb-3; }
.prose p { @apply mb-4 leading-relaxed; }
.prose ul { @apply list-disc list-inside mb-4; }
.prose ol { @apply list-decimal list-inside mb-4; }
.prose a { @apply text-blue-600 hover:underline; }
.prose blockquote { @apply border-l-4 border-gray-300 pl-4 italic text-gray-600 my-4; }
.prose code { @apply bg-gray-100 px-1 py-0.5 rounded font-mono text-sm; }
.prose pre { @apply bg-gray-900 text-white p-4 rounded overflow-x-auto my-4; }
</style>