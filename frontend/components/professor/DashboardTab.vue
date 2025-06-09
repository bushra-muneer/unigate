<script setup lang="ts">
import CourseCard from '@/components/CourseCard.vue';
import CourseSearchBox from '@/components/CourseSearchBox.vue';
import ExamDateDropdown from '@/components/ExamDateDropdown.vue';
import GroupCreationChart from '@/components/GroupCreationChart.vue';
import LoadingIndicator from '@/components/LoadingIndicator.vue';
import { useGroups } from '@/composables/useGroups';
import { computed, onMounted, ref, watch } from 'vue';

const {
  getProfessorsCourses,
  getGroupCount,
  getAverageMembers,
  getActiveGroupCount,
  getGroupCreationDistribution,
  getYearlyStats,
} = useGroups();

const course = ref('');
const examDate = ref('');
const isLoading = ref(true);
const errorMessage = ref('');
const courses = ref<any[]>([]);
const selectedCourseExamDates = ref<string[]>([]);
const groupCounts = ref<Record<string, number>>({});
const averageMembers = ref<Record<string, number>>({});
const activeGroupsCounts = ref<Record<string, Record<string, number>>>({});
const studentNames = ref<string[]>([]);
const groupCreationData = ref<{ date: string; count: number }[]>([]);
const yearlyStats = ref<Record<number, { totalGroups: number; totalMembers: number }>>({});

// Watch course changes to update exam dates
watch(course, (newCourseName) => {
  const matchedCourse = courses.value.find(
    (c) => c.name.toLowerCase() === newCourseName.toLowerCase()
  );
  selectedCourseExamDates.value = matchedCourse?.exams.map((e: any) => e.date) || [];
  examDate.value = '';
});

// Fetch functions
const fetchProfessorsCourses = async () => {
  try {
    const response = await getProfessorsCourses();
    courses.value = response.map((course: any, index: number) => ({
      id: index,
      name: course.name,
      exams: course.exams,
    }));
    await fetchGroupCounts();
    await fetchAverageMembers();
    // await fetchNumberOfActiveGroups();
  } catch (error: any) {
    console.error('Error fetching courses:', error);
    errorMessage.value = error.response?.status === 403
      ? 'Access to this page is blocked. You must be authenticated.'
      : 'Error fetching courses. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

const fetchGroupCounts = async () => {
  for (const course of courses.value) {
    try {
      const response = await getGroupCount(course.name);
      groupCounts.value[course.name] = response.count;
    } catch {
      groupCounts.value[course.name] = 0;
    }
  }
};

const fetchAverageMembers = async () => {
  for (const course of courses.value) {
    try {
      const response = await getAverageMembers(course.name);
      averageMembers.value[course.name] = response.avg;
    } catch {
      averageMembers.value[course.name] = 0;
    }
  }
};

// const fetchNumberOfActiveGroups = async () => {
//   for (const course of courses.value) {
//     activeGroupsCounts.value[course.name] = {};
//     for (const exam of course.exams) {
//       try {
//         const response = await getActiveGroupCount(course.name, exam.date);
//         activeGroupsCounts.value[course.name][exam.date] = response.groups.filter(
//           (g: any) => g.students.length > 1
//         ).length;
//         if (course.name === course.value && exam.date === examDate.value) {
//           studentNames.value = response.student_names;
//         }
//       } catch {
//         activeGroupsCounts.value[course.name][exam.date] = 0;
//       }
//     }
//   }
// };

const fetchGroupCreationData = async (courseName: string) => {
  try {
    const response = await getGroupCreationDistribution(courseName);
    const creationCounts: Record<string, number> = {};
    response.groups_info.forEach((group: any) => {
      const date = group.creation_date.split('T')[0];
      creationCounts[date] = (creationCounts[date] || 0) + 1;
    });
    groupCreationData.value = Object.entries(creationCounts).map(([date, count]) => ({
      date,
      count,
    }));
  } catch (error) {
    console.error('Error fetching group creation data:', error);
  }
};

const fetchYearlyStats = async () => {
  try {
    const response = await getYearlyStats(course.value);
    yearlyStats.value = response;
  } catch (error) {
    console.error('Error fetching yearly stats:', error);
  }
};

// Watch course + date to fetch student names
watch([course, examDate], async ([newCourse, newExamDate]) => {
  if (newCourse && newExamDate) {
    try {
      const response = await getActiveGroupCount(newCourse, newExamDate);
      studentNames.value = response.student_names;
    } catch {
      studentNames.value = [];
    }
  }
});

const filteredCourses = computed(() =>
  courses.value.filter((c) => c.name.toLowerCase() === course.value.toLowerCase())
);

const currentActiveGroupCount = computed(() => {
  if (!course.value || !examDate.value) return 0;
  return activeGroupsCounts.value[course.value]?.[examDate.value] || 0;
});

onMounted(fetchProfessorsCourses);
</script>

<template>
  <div>
    <LoadingIndicator v-if="isLoading" />
    <div v-else-if="errorMessage" class="text-center text-red-600">
      {{ errorMessage }}
    </div>
    <div v-else>
      <div class="mb-6">
        <CourseSearchBox
          :items="courses"
          placeholder="Enter course name"
          v-model="course"
          @select="async (selected) => {
            course = selected.name;
            examDate.value = '';
            selectedCourseExamDates.value = selected.exams.map((e: any) => e.date);
            await fetchGroupCreationData(course);
            await fetchYearlyStats();
          }"
        />
      </div>

      <div class="mb-6">
        <ExamDateDropdown
          :examDates="selectedCourseExamDates"
          v-model:selectedDate="examDate"
          :disabled="selectedCourseExamDates.length === 0"
        />
      </div>

      <div v-if="filteredCourses.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <CourseCard
          v-for="c in filteredCourses"
          :key="c.id"
          :course="c"
          :groupCount="groupCounts[c.name] || 0"
          :avgMembers="averageMembers[c.name] || 0"
          :activeGroupCount="currentActiveGroupCount"
        />
      </div>
      <div v-else class="text-center text-gray-400 mt-8">
        Select a course to view details
      </div>

<!--<div v-if="studentNames.length" class="mt-8">
        <h2 class="text-xl font-semibold mb-2">Enrolled Students</h2>
        <ul class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
          <li v-for="name in studentNames" :key="name" class="bg-white shadow rounded p-2">
            {{ name }}
          </li>
        </ul>
      </div>-->

      <div v-if="groupCreationData.length" class="mt-8">
        <h2 class="text-xl font-semibold mb-2">Group Creation Over Time</h2>
        <GroupCreationChart :data="groupCreationData" />
      </div>

      <div v-if="Object.keys(yearlyStats).length" class="mt-8">
        <h2 class="text-xl font-semibold mb-2">Yearly Enrollment</h2>
        <table class="w-full table-auto border border-gray-200">
          <thead>
            <tr>
              <th class="border px-4 py-2">Year</th>
              <th class="border px-4 py-2">Total Groups</th>
              <th class="border px-4 py-2">Total Members</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stats, year) in yearlyStats" :key="year">
              <td class="border px-4 py-2">{{ year }}</td>
              <td class="border px-4 py-2">{{ stats.totalGroups }}</td>
              <td class="border px-4 py-2">{{ stats.totalMembers }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
