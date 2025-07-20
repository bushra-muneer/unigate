<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps<{
  courseId: string|number;
  examDate: string;
  data: Array<{ year: string; totalGroups: number; totalMembers: number; exam_date?: string }>;
  isLoading: boolean;
}>();
</script>

<template>
  <div>
    <div v-if="isLoading" class="text-center py-8">Loading yearly stats...</div>
    <table v-else class="table-auto w-full text-left border-collapse border border-gray-200">
      <thead>
        <tr>
          <th class="border border-gray-300 px-4 py-2">Year</th>
          <th class="border border-gray-300 px-4 py-2">Total Groups</th>
          <th class="border border-gray-300 px-4 py-2">Total Members</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in data" :key="row.year">
          <td class="border border-gray-300 px-4 py-2">{{ row.year }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ row.totalGroups }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ row.totalMembers }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template> 