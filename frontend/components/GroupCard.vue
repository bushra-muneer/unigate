<script setup lang="ts">
import { useRouter } from "vue-router";
import { format } from "date-fns";

const props = defineProps<{
  group: {
    id: string;
    name: string;
    type?: "Public" | "Private";
    date?: string;
    description: string;
    exam_date?: string; // student
    examDate?: string;  // professor
    courseName?: string;
    course_name?: string;
    members_count?: number; // student
    member_count?: number;  // professor
    tags?: string[];
    [key: string]: any;
  };
}>();

const router = useRouter();

function formatDate(date: string) {
  try {
    return format(new Date(date), "dd/MM/yyyy");
  } catch {
    return date;
  }
}

function goToGroupPage() {
  router.push(`/groups/${props.group.id}`);
}

const memberCount = props.group.member_count ?? props.group.members_count ?? 0;
const examDate = props.group.examDate ?? props.group.exam_date ?? props.group.date ?? "";
const courseName = props.group.courseName ?? props.group.course_name ?? "";
const groupType = props.group.type ?? "Public";
const name = props.group.name;
const description = props.group.description;
const tags = props.group.tags ?? [];
</script>

<template>
  <div
    class="bg-gray-100 rounded-lg shadow p-4 flex flex-col justify-between h-48 w-full cursor-pointer transition-shadow hover:shadow-lg hover:bg-gray-200 select-none"
    @click="goToGroupPage"
    tabindex="0"
    @keydown.enter="goToGroupPage"
    :aria-label="`View details for group ${name}`"
    role="button"
  >
    <div>
      <div class="flex items-start space-x-1 font-semibold text-gray-800 text-sm mb-1">
        <span>
          <svg
            v-if="groupType === 'Public'"
            xmlns="http://www.w3.org/2000/svg"
            class="w-4 h-4 text-gray-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 17a2 2 0 002-2v-2a2 2 0 00-4 0v2a2 2 0 002 2zm6-6V9a6 6 0 10-12 0v2a2 2 0 00-2 2v7a2 2 0 002 2h12a2 2 0 002-2v-7a2 2 0 00-2-2zm-8-2a4 4 0 118 0v2H6V9z"
            />
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            class="w-4 h-4 text-gray-500"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              d="M12 17a2 2 0 002-2v-2a2 2 0 00-4 0v2a2 2 0 002 2zm6-6V9a6 6 0 10-12 0v2a2 2 0 00-2 2v7a2 2 0 002 2h12a2 2 0 002-2v-7a2 2 0 00-2-2zm-8-2a4 4 0 118 0v2H6V9z"
            />
          </svg>
        </span>
        <span class="line-clamp-2">{{ name }}</span>
      </div>
      <p class="text-xs text-gray-600">{{ description }}</p>
    </div>
    <div>
      <span class="inline-block bg-gray-300 text-gray-800 rounded px-2 py-0.5 text-xs font-medium mb-2">
        {{ tags.length ? tags[0] : courseName }}
      </span>
    </div>
    <div class="flex justify-between items-center text-sm text-gray-600 mt-4">
      <div class="flex items-center gap-1">
        <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M13 7a3 3 0 11-6 0 3 3 0 016 0zM4 14s1-1 6-1 6 1 6 1v1H4v-1z" />
        </svg>
        <span>{{ memberCount }}</span>
      </div>
      <div class="flex items-center gap-1">
        <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M6 2a1 1 0 011 1v1h6V3a1 1 0 112 0v1a2 2 0 012 2v10a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2V3a1 1 0 011-1z" />
        </svg>
        <span>{{ formatDate(examDate) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bg-gray-100:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
</style>
