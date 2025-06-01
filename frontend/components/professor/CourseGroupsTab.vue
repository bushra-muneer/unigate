<template>
  <div class="p-8 relative">
    <h2 class="text-2xl font-semibold mb-4">Course Groups</h2>

    <div v-if="isLoading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>

    <div v-else v-for="course in coursesWithGroups" :key="course.courseId" class="mb-6 border rounded-lg p-4">
      <div @click="toggleCourse(course.courseId)" class="cursor-pointer font-bold">
        {{ isCourseExpanded(course.courseId) ? '▼' : '▶' }} {{ course.courseName }} ({{ course.groups.length }} Groups)
      </div>

      <div v-show="isCourseExpanded(course.courseId)" class="pl-4 mt-2">
        <div v-for="status in groupByStatus(course.groups).order" :key="status">
          <div v-if="groupByStatus(course.groups).map[status]">
            <div @click="toggleStatus(course.courseId, status)" class="cursor-pointer font-semibold">
              {{ isStatusExpanded(course.courseId, status) ? '▼' : '▶' }} {{ status }} ({{ groupByStatus(course.groups).map[status].length }} Groups)
            </div>
            <div v-show="isStatusExpanded(course.courseId, status)" class="pl-4 mt-1">
              <div
                v-for="(dateGroups, date) in groupByDate(groupByStatus(course.groups).map[status])"
                :key="date"
                class="mb-2"
              >
                <div @click="toggleStatus(status, date)" class="cursor-pointer text-sm text-gray-600 mb-1">
                  {{ isStatusExpanded(status, date) ? '▼' : '▶' }} Exam Date: {{ formatDate(date) }} ({{ dateGroups.length }} Groups)
                </div>
                <div v-show="isStatusExpanded(status, date)" class="flex space-x-4 overflow-x-auto">
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

  
  </div>
</template>

<script setup lang="ts">
import { useGroups } from '@/composables/useGroups';
import { format } from 'date-fns';
import { onMounted, ref } from 'vue';
import GroupCard from './GroupCardComp.vue';

interface Group {
  id: string;
  name: string;
  type: string;
  date: string;
  description: string;
  examDate: string;
  courseName: string;
  tags: string[];
  member_count?: number;
  status?: string;
}

interface CourseWithGroups {
  courseId: string;
  courseName: string;
  groups: Group[];
}

const carousel = ref<HTMLDivElement | null>(null);
const coursesWithGroups = ref<CourseWithGroups[]>([]);
const expandedCourses = ref<string[]>([]);
const expandedStatuses = ref<Record<string, string[]>>({});
const isLoading = ref(false);

const { getCoursesWithGroups, getGroupMemberCount } = useGroups();

async function fetchGroupsWithMemberCounts() {
  try {
    isLoading.value = true;
    const res = await getCoursesWithGroups() as CourseWithGroups[];
    // Для каждой группы получаем member_count
    for (const course of res) {
      for (const group of course.groups) {
        console.log('group:', group);
        group.member_count = await getGroupMemberCount(group.id);
      }
    }
    coursesWithGroups.value = res;
  } catch (error) {
    console.error('Failed to fetch courses with groups:', error);
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchGroupsWithMemberCounts();
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

function groupByStatus(groups: Group[]) {
  const map: Record<string, Group[]> = {};
  for (const g of groups) {
    const key = g.status || 'UNKNOWN';
    if (!map[key]) map[key] = [];
    map[key].push(g);
  }
  return {
    map,
    order: ['Active', 'Recently Over', 'Inactive', 'UNKNOWN']
  };
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
