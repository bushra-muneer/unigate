<!-- GroupCard.vue -->
<template>
  <div class="bg-gray-100 rounded-lg shadow p-4 flex flex-col justify-between h-48 w-full">
    <div>
      <div class="flex items-start space-x-1 font-semibold text-gray-800 text-sm mb-1">
        <span class="text-yellow-500">⚡</span>
        <span class="line-clamp-2">{{ group.name }}</span>
      </div>
      
      <p class="text-xs text-gray-600">{{ group.description }}</p>
    </div>
    <div class="flex justify-between items-center text-sm text-gray-600 mt-4">
      <div class="flex items-center gap-1">
        <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M13 7a3 3 0 11-6 0 3 3 0 016 0zM4 14s1-1 6-1 6 1 6 1v1H4v-1z" />
        </svg>
        <span>{{ group.memberCount }}</span>
      </div>
      <div class="flex items-center gap-1">
        <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M6 2a1 1 0 011 1v1h6V3a1 1 0 112 0v1a2 2 0 012 2v10a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2V3a1 1 0 011-1z" />
        </svg>
        <span>{{ group.date }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  group: {
    name: string;
    description: string;
    memberCount: number;
    date: string;
  };
}>();
</script>
