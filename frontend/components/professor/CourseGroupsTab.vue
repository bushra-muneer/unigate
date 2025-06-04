<template>
  <div class="p-8 relative">
    <h2 class="text-2xl font-semibold mb-4">Course Groups</h2>

    <!-- Search Input -->
    <div class="mb-4 relative">
      <input
        type="text"
        placeholder="Search by Group Name, Course Name"
        class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        v-model="searchQuery"
      />
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-500"
      >
        ✕
      </button>
    </div>
    <!-- End Search Input -->

    <div v-for="course in filteredCoursesWithGroups" :key="course.courseId" class="mb-6 border rounded-lg p-4">
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

    <!-- No Results Found Message -->
    <div v-if="filteredCoursesWithGroups.length === 0 && searchQuery">
      <p class="text-center text-gray-500">No results found.</p>
    </div>
    <!-- End No Results Found Message -->

  
  </div>
</template>

<script setup lang="ts">
import { useGroups } from '@/composables/useGroups';
import { format } from 'date-fns';
import { computed, onMounted, ref } from 'vue';
import GroupCard from './GroupCardComp.vue';

interface Group {
  id: string;
  name: string;
  type: string;
  examDate: string;
  description: string;
  memberCount: number;
  date: string;
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
const searchQuery = ref('');

const { getCoursesWithGroups } = useGroups();

onMounted(async () => {
  try {
    const res = await getCoursesWithGroups();
    coursesWithGroups.value = res as CourseWithGroups[];
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

function groupByType(groups: Group[]) {
  const map: Record<string, Group[]> = {};
  for (const g of groups) {
    const key = g.type || 'Unknown';
    if (!map[key]) map[key] = [];
    map[key].push(g);
  }
  return map;
}

function groupByDate(groups: Group[]) {
  const map: Record<string, Group[]> = {};
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

function clearSearch() {
  searchQuery.value = '';
}

// Computed property for filtering courses and groups
const filteredCoursesWithGroups = computed(() => {
  if (!searchQuery.value) {
    // Map examDate to date and format for the original coursesWithGroups when no search query
    return coursesWithGroups.value.map(course => ({
      ...course,
      groups: course.groups.map(group => ({
        ...group,
        date: formatDate(group.examDate),
      })),
    }));
  }
  const lowerCaseQuery = searchQuery.value.toLowerCase();

  return coursesWithGroups.value.map(course => {
    const filteredGroups = course.groups.filter(group => {
      // Check if group name or course name includes the search query
      return group.name.toLowerCase().includes(lowerCaseQuery) ||
             course.courseName.toLowerCase().includes(lowerCaseQuery);
    }).map(group => ({ // Map to the structure expected by GroupCardComp.vue, including formatted date
      ...group,
      date: formatDate(group.examDate), // Map examDate to date and format it
    }));

    // Only include courses that have at least one matching group, or if the course name itself matches
    if (filteredGroups.length > 0 || course.courseName.toLowerCase().includes(lowerCaseQuery)) {
      return { ...course, groups: filteredGroups };
    } else {
      return null; // Exclude courses with no matching groups and no matching course name
    }
  }).filter(course => course !== null) as CourseWithGroups[]; // Remove null entries and cast
});
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
