<template>
  <div class="p-8 relative">
    <h2 class="text-2xl font-semibold mb-4">Course Groups</h2>

    <!-- Left Arrow -->
    <button
      class="absolute left-0 top-[50%] -translate-y-1/2 z-10 bg-white shadow p-2 rounded-full"
      @click="scrollLeft"
    >
      <span class="text-lg">&lt;</span>
    </button>

    <!-- Right Arrow -->
    <button
      class="absolute right-0 top-[50%] -translate-y-1/2 z-10 bg-white shadow p-2 rounded-full"
      @click="scrollRight"
    >
      <span class="text-lg">&gt;</span>
    </button>

    <!-- Carousel -->
    <div
      ref="carousel"
      class="overflow-x-auto scrollbar-hide scroll-smooth"
    >
      <div class="flex space-x-4 min-w-max">
        <GroupCard
          v-for="group in allGroups"
          :key="group.id"
          :group="group"
          class="min-w-[250px] max-w-[250px] flex-shrink-0"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import GroupCard from './GroupCardComp.vue';

const carousel = ref<HTMLDivElement | null>(null);

function scrollLeft() {
  carousel.value?.scrollBy({ left: -300, behavior: 'smooth' });
}

function scrollRight() {
  carousel.value?.scrollBy({ left: 300, behavior: 'smooth' });
}

const allGroups = [
  {
    id: '1',
    name: 'Design Sprint Team',
    description: 'Collaborative UX and product design team.',
    memberCount: 5,
    date: '14/02/2025',
  },
  {
    id: '2',
    name: 'Frontend Ninjas',
    description: 'React and UI/UX team.',
    memberCount: 9,
    date: '16/02/2025',
  },
  {
    id: '3',
    name: 'AI Enthusiasts Group',
    description: 'Focusing on ML, AI, and Data Science projects.',
    memberCount: 8,
    date: '13/02/2025',
  },
  {
    id: '4',
    name: 'Brand Strategy Crew',
    description: 'Designers working on branding initiatives.',
    memberCount: 7,
    date: '15/02/2025',
  },
  {
    id: '5',
    name: 'Design Pioneers',
    description: 'UX researchers and interaction designers.',
    memberCount: 6,
    date: '17/02/2025',
  },
   {
    id: '6',
    name: 'Design Pioneers',
    description: 'UX researchers and interaction designers.',
    memberCount: 6,
    date: '17/02/2025',
  },
   {
    id: '7',
    name: 'Design Pioneers',
    description: 'UX researchers and interaction designers.',
    memberCount: 6,
    date: '17/02/2025',
  },
];
</script>

<style>
/* Optional: Hide scrollbar on all browsers */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
