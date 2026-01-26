<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ArrowLeft } from 'lucide-vue-next';
import axios from 'axios';
import { marked } from 'marked';

const router = useRouter();
const articles = ref<any[]>([]);

onMounted(async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/seo-articles/');
        articles.value = response.data;
    } catch (e) {
        console.error("Failed to fetch articles", e);
    }
});

const renderMarkdown = (content: string) => {
    return marked(content);
};
</script>

<template>
    <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
        <!-- Header -->
        <header class="bg-white shadow-md sticky top-0 z-50">
            <div class="container mx-auto px-4 py-4 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <button @click="router.push('/')" class="text-gray-600 hover:text-saffron transition-colors">
                        <ArrowLeft class="w-6 h-6" />
                    </button>
                    <h1 class="text-2xl font-bold text-navy-blue font-serif">SEO Class</h1>
                </div>
            </div>
        </header>

        <!-- Content -->
        <main class="container mx-auto px-4 py-8 max-w-4xl">
            <div v-if="articles.length === 0" class="text-center py-20 text-gray-500">
                <p class="text-xl">No articles available yet. Stay tuned!</p>
            </div>

            <div v-else class="space-y-12">
                <article v-for="article in articles" :key="article.id" class="bg-white rounded-xl shadow-lg overflow-hidden p-8">
                    <h2 class="text-3xl font-bold text-navy-blue mb-4">{{ article.title }}</h2>
                    <div class="text-gray-500 text-sm mb-6 pb-4 border-b">
                        Published on {{ new Date(article.created_at).toLocaleDateString() }}
                    </div>
                    <div class="prose prose-lg max-w-none text-gray-700" v-html="renderMarkdown(article.content)"></div>
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