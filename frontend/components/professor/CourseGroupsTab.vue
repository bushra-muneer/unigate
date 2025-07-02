<template>
  <div class="p-8 relative">
    <h2 class="text-2xl font-semibold mb-4">Course Groups</h2>

    <!-- Search Input -->
    <div class="mb-4 relative">
      <input
        type="text"
        placeholder="Search by Group Name, Course Name, or Tags (use spaces for multiple tags)"
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

    <div v-if="isLoading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>

    <div
      v-else
      v-for="course in filteredCoursesWithGroups"
      :key="course.courseId"
      class="mb-6 border rounded-lg p-4"
    >
      <div
        @click="toggleCourse(course.courseId)"
        class="cursor-pointer font-bold"
      >
        {{ isCourseExpanded(course.courseId) ? "▼" : "▶" }}
        {{ course.courseName }} ({{ course.groups.length }} Groups)
      </div>

      <div v-show="isCourseExpanded(course.courseId)" class="pl-4 mt-2">
        <div v-for="status in groupByStatus(course.groups).order" :key="status">
          <div v-if="groupByStatus(course.groups).map[status]">
            <div
              @click="toggleStatus(course.courseId, status)"
              class="cursor-pointer font-semibold"
            >
              {{ isStatusExpanded(course.courseId, status) ? "▼" : "▶" }}
              {{ status }} ({{ groupByStatus(course.groups).map[status].length }} Groups)
            </div>
            <div
              v-show="isStatusExpanded(course.courseId, status)"
              class="pl-4 mt-1"
            >
              <div
                v-for="(dateGroups, date) in groupByDate(groupByStatus(course.groups).map[status])"
                :key="date"
                class="mb-2"
              >
                <div class="flex justify-between items-center mb-2">
                  <div
                    @click="toggleStatus(status, date)"
                    class="cursor-pointer text-sm text-gray-600"
                  >
                    {{ isStatusExpanded(status, date) ? "▼" : "▶" }} Exam Date:
                    {{ formatDate(date) }} ({{ dateGroups.length }} Groups)
                  </div>

                  <div class="flex items-center space-x-2">
                    <span class="text-sm font-medium text-gray-700">Sort by:</span>
                    <select
                      v-model="selectedSorts[`${status}_${date}`]"
                      class="border rounded px-2 py-1 text-sm"
                    >
                      <option value="creation">Creation Date</option>
                      <option value="asc">Members - ASC</option>
                      <option value="desc">Members - DESC</option>
                    </select>
                  </div>
                </div>

                <div v-show="isStatusExpanded(status, date)" class="flex flex-col">
                  <div class="flex space-x-4 overflow-x-auto">
                    <GroupCard
                      v-for="group in getSortedGroups(status, date, dateGroups).slice(0, getCurrentLimit(status, date))"
                      :key="group.id"
                      :group="group"
                      class="min-w-[250px] max-w-[250px] flex-shrink-0"
                    />
                    <button
                      v-if="dateGroups.length > getCurrentLimit(status, date)"
                      @click="showMore(status, date)"
                      class="min-w-[125px] max-w-[125px] flex-shrink-0 flex items-center justify-center border-2 border-gray-700 text-gray-800 font-semibold text-base rounded-full bg-white hover:bg-gray-100 transition shadow"
                      style="height: 48px; margin-top: auto; margin-bottom: auto;"
                    >
                      Show more
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Results Found -->
    <div
      v-if="!isLoading && filteredCoursesWithGroups.length === 0 && searchQuery"
    >
      <p class="text-center text-gray-500">No results found.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGroups } from "@/composables/useGroups";
import { format } from "date-fns";
import { computed, onMounted, ref } from "vue";
import GroupCard from "./GroupCardComp.vue";

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
const groupCardLimit = ref<Record<string, number>>({});
const selectedSorts = ref<Record<string, string>>({});
const searchQuery = ref("");

const { getCoursesWithGroups, getGroupMemberCount } = useGroups();

async function fetchGroupsWithMemberCounts() {
  try {
    isLoading.value = true;
    const res = (await getCoursesWithGroups()) as CourseWithGroups[];
    for (const course of res) {
      for (const group of course.groups) {
        group.member_count = await getGroupMemberCount(group.id);
      }
    }
    coursesWithGroups.value = res;
  } catch (error) {
    console.error("Failed to fetch courses with groups:", error);
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchGroupsWithMemberCounts();
});

function getSortedGroups(status: string, date: string, groups: Group[]) {
  const sortKey = `${status}_${date}`;
  const selectedSort = selectedSorts.value[sortKey] || "creation";
  const sorted = [...groups];

  if (selectedSort === "asc") {
    sorted.sort((a, b) => (a.member_count ?? 0) - (b.member_count ?? 0));
  } else if (selectedSort === "desc") {
    sorted.sort((a, b) => (b.member_count ?? 0) - (a.member_count ?? 0));
  }

  return sorted;
}

function groupByDate(groups: any[]) {
  const map: Record<string, any[]> = {};
  for (const g of groups) {
    const key = g.examDate || "No Date";
    if (!map[key]) map[key] = [];
    map[key].push(g);
  }
  return map;
}

function formatDate(dateStr: string) {
  try {
    return format(new Date(dateStr), "dd/MM/yyyy");
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
    const key = g.status || "UNKNOWN";
    if (!map[key]) map[key] = [];
    map[key].push(g);
  }
  return {
    map,
    order: ["Active", "Recently Over", "Inactive", "UNKNOWN"],
  };
}

function getLimitKey(status: string, date: string) {
  return `${status}_${date}`;
}

function getCurrentLimit(status: string, date: string) {
  return groupCardLimit.value[getLimitKey(status, date)] ?? 5;
}

function showMore(status: string, date: string) {
  const key = getLimitKey(status, date);
  groupCardLimit.value[key] = getCurrentLimit(status, date) + 5;
}

function clearSearch() {
  searchQuery.value = "";
}

const filteredCoursesWithGroups = computed(() => {
  if (!searchQuery.value) return coursesWithGroups.value;

  const tokens = searchQuery.value.trim().toLowerCase().split(/\s+/);
  const multiple = tokens.length > 1;

  return coursesWithGroups.value
    .map((course) => {
      const filteredGroups = course.groups.filter((group) => {
        if (multiple) {
          return tokens.every((t) =>
            group.tags?.some((tag) => tag.toLowerCase().includes(t)),
          );
        }

        const query = tokens[0];
        return (
          group.name.toLowerCase().includes(query) ||
          course.courseName.toLowerCase().includes(query) ||
          group.tags?.some((tag) => tag.toLowerCase().includes(query))
        );
      });

      if (
        filteredGroups.length > 0 ||
        (!multiple && course.courseName.toLowerCase().includes(tokens[0]))
      ) {
        return {
          ...course,
          groups: filteredGroups,
        };
      }
      return null;
    })
    .filter((course): course is CourseWithGroups => course !== null);
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
