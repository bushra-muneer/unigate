<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import ExamDateDropdown from '@/components/ExamDateDropdown.vue';
import GroupCreationChart from '@/components/GroupCreationChart.vue';
import YearlyEnrollmentTable from '@/components/YearlyEnrollmentTable.vue';
import LoadingIndicator from '@/components/LoadingIndicator.vue';
import { useGroups } from '@/composables/useGroups';

const SELECTED_COURSE_KEY = 'unigate_selected_course';
const { getProfessorsCourses, getGroupCreationDistribution, getYearlyStats } = useGroups();
const courses = ref<Array<{ id: string|number, name: string, exams: { date: string }[] }>>([]);
const isLoading = ref(true);
const errorMessage = ref('');

// Course selection with localStorage persistence
const selectedCourseId = ref('');
const selectedCourse = computed(() => courses.value.find(c => String(c.id) === String(selectedCourseId.value)));

// Per-widget exam date state
const groupCreationExamDate = ref('All');
const yearlyEnrollmentExamDate = ref('All');

// Reset exam dates when course changes
watch(selectedCourseId, () => {
  groupCreationExamDate.value = 'All';
  yearlyEnrollmentExamDate.value = 'All';
});

// Fetch professor's courses from the API
const fetchProfessorsCourses = async () => {
  try {
    const response = await getProfessorsCourses();
    courses.value = (response as any).map((course: any) => ({
      id: course.id ?? course.name,
      name: course.name,
      exams: course.exams,
    }));
    initializeSelectedCourse();
  } catch (error: any) {
    errorMessage.value = 'Error fetching courses. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

function initializeSelectedCourse() {
  if (typeof window === 'undefined') return;
  const saved = localStorage.getItem(SELECTED_COURSE_KEY);
  const sortedCourses = [...courses.value].sort((a, b) => a.name.localeCompare(b.name));
  if (saved && courses.value.some(c => String(c.id) === saved)) {
    selectedCourseId.value = saved;
  } else if (sortedCourses.length) {
    selectedCourseId.value = String(sortedCourses[0].id);
  }
}

// Persist course selection
watch(selectedCourseId, (val) => {
  if (val && typeof window !== 'undefined') {
    localStorage.setItem(SELECTED_COURSE_KEY, String(val));
  }
});

onMounted(fetchProfessorsCourses);

const groupCreationExamDates = computed(() => {
  if (selectedCourse.value && selectedCourse.value.exams) {
    const dates = selectedCourse.value.exams.map((e: { date: string }) => e.date);
    const uniqueDates = Array.from(new Set(dates));
    return ['All', ...uniqueDates];
  }
  return ['All'];
});
const yearlyEnrollmentExamDates = groupCreationExamDates;

// --- Patch GroupCreationChart and YearlyEnrollmentTable to use real API ---
const groupCreationChartData = ref<any[]>([]);
const groupCreationChartLoading = ref(false);
watch([selectedCourseId, groupCreationExamDate], async () => {
  if (!selectedCourse.value) return;
  groupCreationChartLoading.value = true;
  try {
    const courseName = selectedCourse.value.name;
    const data = await getGroupCreationDistribution(courseName) as { groups_info?: any[] };
    const groupsInfo = (data && Array.isArray(data.groups_info)) ? data.groups_info : [];
    // Filter by exam date (string match)
    const filtered = groupsInfo.filter((item: any) =>
      groupCreationExamDate.value === 'All' || item.exam_date === groupCreationExamDate.value
    );
    // Aggregate by creation_date (YYYY-MM-DD)
    const dateMap: Record<string, number> = {};
    filtered.forEach((item: any) => {
      if (!item.creation_date) return;
      const dateStr = item.creation_date.split('T')[0]; // "YYYY-MM-DD"
      dateMap[dateStr] = (dateMap[dateStr] || 0) + 1;
    });
    groupCreationChartData.value = Object.entries(dateMap).map(([date, count]) => ({
      creation_date: date,
      count,
    }));
  } catch (e) {
    groupCreationChartData.value = [];
  } finally {
    groupCreationChartLoading.value = false;
  }
}, { immediate: true });

const yearlyEnrollmentTableData = ref<any[]>([]);
const yearlyEnrollmentTableLoading = ref(false);
watch([selectedCourseId, yearlyEnrollmentExamDate], async () => {
  if (!selectedCourse.value) return;
  yearlyEnrollmentTableLoading.value = true;
  try {
    const courseName = selectedCourse.value.name;
    const data = await getYearlyStats(courseName);
    const yearlyStatsArr = data && typeof data === 'object' ? Object.entries(data).map(([year, stats]: [string, any]) => ({ year, ...stats })) : [];
    yearlyEnrollmentTableData.value = yearlyStatsArr.filter((item: any) => yearlyEnrollmentExamDate.value === 'All' || item.exam_date === yearlyEnrollmentExamDate.value);
  } catch (e) {
    yearlyEnrollmentTableData.value = [];
  } finally {
    yearlyEnrollmentTableLoading.value = false;
  }
}, { immediate: true });
</script>

<template>
  <div>
    <LoadingIndicator v-if="isLoading" />
    <div v-else-if="errorMessage" class="text-center text-red-500 py-8">
      {{ errorMessage }}
    </div>
    <div v-else class="flex flex-col items-center min-h-[80vh] bg-gray-100 py-6">
      <div class="container mx-auto max-w-5xl bg-white shadow-lg rounded-lg p-8 overflow-y-auto">
        <!-- Course Dropdown at the top left -->
        <div class="flex justify-between items-center mb-8">
          <div class="w-80">
            <label for="courseDropdown" class="block mb-2 text-sm font-medium text-gray-700">Course Name</label>
            <select
              id="courseDropdown"
              v-model="selectedCourseId"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
            >
              <option v-for="course in courses" :key="course.id" :value="String(course.id)">
                {{ course.name }}
              </option>
            </select>
          </div>
        </div>
        <!-- Group Creation Chart Widget with Exam Date Filter -->
        <div class="mb-12">
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-2xl font-bold">Group Creation Over Time</h2>
            <div class="w-64">
              <ExamDateDropdown
                :dates="groupCreationExamDates"
                v-model="groupCreationExamDate"
              />
            </div>
          </div>
          <GroupCreationChart
            :courseId="selectedCourseId"
            :examDate="groupCreationExamDate"
            :data="groupCreationChartData"
            :isLoading="groupCreationChartLoading"
          />
        </div>
        <!-- Yearly Enrollment Table Widget with Exam Date Filter -->
        <div class="mb-2">
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-2xl font-bold">Yearly Group Enrollment and Participation</h2>
            <div class="w-64">
              <ExamDateDropdown
                :dates="yearlyEnrollmentExamDates"
                v-model="yearlyEnrollmentExamDate"
              />
            </div>
          </div>
          <YearlyEnrollmentTable
            :courseId="selectedCourseId"
            :examDate="yearlyEnrollmentExamDate"
            :data="yearlyEnrollmentTableData"
            :isLoading="yearlyEnrollmentTableLoading"
          />
        </div>
      </div>
    </div>
  </div>
</template>
