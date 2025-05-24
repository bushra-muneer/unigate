<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import TabSwitcher from '@/components/TabSwitcher.vue';
import DashboardTab from '@/components/professor/DashboardTab.vue';
import CourseGroupsTab from '@/components/professor/CourseGroupsTab.vue';

const route = useRoute();
const router = useRouter();

const tabs = [

  { key: 'dashboard', label: 'Dashboard' },
    { key: 'groups', label: 'Course Groups' },
];

const activeTab = ref<'dashboard' | 'groups'>('dashboard');

onMounted(() => {
  const tabFromQuery = route.query.tab as string;
  if (tabFromQuery === 'groups' || tabFromQuery === 'dashboard') {
    activeTab.value = tabFromQuery;
  } else {
    activeTab.value = 'dashboard';
    router.replace({ query: { tab: 'dashboard' } }); 
  }
});

// // Update URL when tab changes
// watch(activeTab, (newTab) => {
//   router.replace({ query: { tab: newTab } });
// });
</script>

<template>
  <div class="container mx-auto px-4">
    <TabSwitcher v-model="activeTab" :tabs="tabs" />

    <DashboardTab v-if="activeTab === 'dashboard'" />
    <CourseGroupsTab v-else-if="activeTab === 'groups'" />
  </div>
</template>
