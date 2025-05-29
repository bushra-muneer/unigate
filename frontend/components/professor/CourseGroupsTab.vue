<template>
  <div class="p-8 relative">
    <h2 class="text-2xl font-semibold mb-4">Course Groups</h2>

    <div v-for="course in coursesWithGroups" :key="course.courseId" class="mb-6 border rounded-lg p-4">
      <div @click="toggleCourse(course.courseId)" class="cursor-pointer font-bold">
        {{ isCourseExpanded(course.courseId) ? '▼' : '▶' }} {{ course.courseName }} ({{ course.groups.length }} Groups)
      </div>

      <div v-show="isCourseExpanded(course.courseId)" class="pl-4 mt-2">
        <div
          v-for="(typeGroups, type) in groupByType(course.groups)"
          :key="type"
          class="mb-3"
        >
          <div @click="toggleStatus(course.courseId, type)" class="cursor-pointer font-semibold">
            {{ isStatusExpanded(course.courseId, type) ? '▼' : '▶' }} {{ type }} ({{ typeGroups.length }} Groups)
          </div>

          <div v-show="isStatusExpanded(course.courseId, type)" class="pl-4 mt-1">
            <div
              v-for="(dateGroups, date) in groupByDate(typeGroups)"
              :key="date"
              class="mb-2"
            >
              <div @click="toggleStatus(type, date)" class="cursor-pointer text-sm text-gray-600 mb-1">
                {{ isStatusExpanded(type, date) ? '▼' : '▶' }} Exam Date: {{ formatDate(date) }} ({{ dateGroups.length }} Groups)
              </div>
              <div v-show="isStatusExpanded(type, date)" class="flex space-x-4 overflow-x-auto">
              
                <GroupCard
                  v-for="group in dateGroups"
                  :key="group.id"
                  :group="group"
                  class="min-w-[250px] max-w-[250px] flex-shrink-0"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { format } from 'date-fns';
import GroupCard from './GroupCardComp.vue';
import { useGroups } from '@/composables/useGroups';

const carousel = ref<HTMLDivElement | null>(null);
const coursesWithGroups = ref([]);
const expandedCourses = ref<string[]>([]);
const expandedStatuses = ref<Record<string, string[]>>({});

const { getCoursesWithGroups } = useGroups();

onMounted(async () => {
  try {
    const res = await getCoursesWithGroups();
    coursesWithGroups.value = res;
  } catch (error) {
    console.error('Failed to fetch courses with groups:', error);
  }
});

function scrollLeft() {
  carousel.value?.scrollBy({ left: -300, behavior: 'smooth' });
}
function scrollRight() {
  carousel.value?.scrollBy({ left: 300, behavior: 'smooth' });
}

function groupByType(groups: any[]) {
  const map: Record<string, any[]> = {};
  for (const g of groups) {
    const key = g.type || 'Unknown';
    if (!map[key]) map[key] = [];
    map[key].push(g);
  }
  return map;
}

function groupByDate(groups: any[]) {
  const map: Record<string, any[]> = {};
  for (const g of groups) {
    const key = g.examDate || 'No Date';
    if (!map[key]) map[key] = [];
    map[key].push(g);
  }
  return map;
}

function formatDate(dateStr: string) {
  try {
    return format(new Date(dateStr), 'dd/MM/yyyy');
  } catch {
    return dateStr;
  }
}

function toggleCourse(courseId: string) {
  const index = expandedCourses.value.indexOf(courseId);
  if (index >= 0) {
    expandedCourses.value.splice(index, 1);
  } else {
    expandedCourses.value.push(courseId);
  }
}

function isCourseExpanded(courseId: string) {
  return expandedCourses.value.includes(courseId);
}

function toggleStatus(parentId: string, childKey: string) {
  if (!expandedStatuses.value[parentId]) expandedStatuses.value[parentId] = [];
  const index = expandedStatuses.value[parentId].indexOf(childKey);
  if (index >= 0) {
    expandedStatuses.value[parentId].splice(index, 1);
  } else {
    expandedStatuses.value[parentId].push(childKey);
  }
}

function isStatusExpanded(parentId: string, childKey: string) {
  return expandedStatuses.value[parentId]?.includes(childKey);
}
</script>

<style>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
