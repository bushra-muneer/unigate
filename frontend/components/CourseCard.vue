<template>
  <div
    class="rounded-lg border bg-card text-card-foreground shadow-sm transition-shadow hover:shadow-md p-4"
  >
    <!-- Course Name and Group Tag -->
    <h2
      id="course_name_card"
      class="text-base font-semibold flex items-center justify-between"
    >
      {{ course.name }}
      <span
        id="course_number_groups"
        class="rounded-full bg-emerald-500 text-white px-2 py-1 text-xs font-medium"
      >
        Groups: {{ groupCount }}
      </span>
    </h2>

    <!-- Average People per Group -->
    <p id="course_avg_members_group" class="text-sm mt-2">
      Average members per group: {{ avgMembers }}
    </p>

    <!-- Number of Active Groups -->
    <p id="course_number_active_groups" class="text-sm mt-2">
      Number of Active Groups: {{ activeGroupCount }}
    </p>

    <!-- Exam List with Expandable Sections -->
    <div class="mt-3 space-y-2">
      <div
        v-for="(exam, index) in course.exams"
        :key="exam.date"
        class="rounded-md border bg-muted/50"
      >
        <!-- Exam Date Header (Clickable) -->
        <button
          @click="toggleExamSection(exam.date)"
          class="w-full flex justify-between items-center p-2 hover:bg-muted/70 transition-colors"
        >
          <span class="text-sm">{{ exam.date }}</span>
          <span class="text-sm">
            {{ isExpanded(exam.date) ? '▼' : '▶' }}
          </span>
        </button>

        <!-- Expanded Content -->
        <div v-if="isExpanded(exam.date)" class="p-2 border-t">
          <!-- Loading State -->
          <div v-if="isLoadingGroups(exam.date)" class="flex justify-center py-2">
            <LoadingIndicator />
          </div>

          <!-- Error State -->
          <div v-else-if="hasError(exam.date)" class="text-red-500 text-sm py-2">
            Failed to load groups
          </div>

          <!-- Groups Grid -->
          <div v-else-if="getGroupsForExam(exam.date).length" class="grid grid-cols-1 gap-2">
            <GroupCard
              v-for="group in getGroupsForExam(exam.date)"
              :key="group.id"
              :group="group"
              class="w-full"
            />
          </div>

          <!-- No Groups State -->
          <div v-else class="text-gray-500 text-sm py-2 text-center">
            No groups found for this exam date
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import GroupCard from "@/components/GroupCard.vue";
import LoadingIndicator from "@/components/LoadingIndicator.vue";
import { useGroups } from "@/composables/useGroups";
import { ref } from "vue";

interface Course {
  id: number;
  name: string;
  exams: {
    date: string;
    groupCount: number;
    avgMembers: number;
    activeGroupCount: number;
  }[];
}

interface Group {
  id: string;
  name: string;
  description: string;
  category: string;
  recentActivity: string;
  members_count: number;
  students: string[];
}

interface ActiveGroupsResponse {
  groups: Group[];
  student_names: string[];
}

const props = defineProps<{
  course: Course;
  groupCount: number;
  avgMembers: number;
  activeGroupCount: number;
}>();

const { getActiveGroupCount } = useGroups();

// State for expanded sections and loaded groups
const expandedSections = ref<Set<string>>(new Set());
const loadedGroups = ref<Record<string, Group[]>>({});
const loadingStates = ref<Record<string, boolean>>({});
const errorStates = ref<Record<string, boolean>>({});

// Toggle exam section expansion
const toggleExamSection = async (examDate: string) => {
  if (expandedSections.value.has(examDate)) {
    expandedSections.value.delete(examDate);
  } else {
    expandedSections.value.add(examDate);
    // Load groups if not already loaded
    if (!loadedGroups.value[examDate] && !loadingStates.value[examDate]) {
      await loadGroupsForExam(examDate);
    }
  }
};

// Check if section is expanded
const isExpanded = (examDate: string) => expandedSections.value.has(examDate);

// Check loading state
const isLoadingGroups = (examDate: string) => loadingStates.value[examDate];

// Check error state
const hasError = (examDate: string) => errorStates.value[examDate];

// Get groups for specific exam date
const getGroupsForExam = (examDate: string) => loadedGroups.value[examDate] || [];

// Load groups for exam date
const loadGroupsForExam = async (examDate: string) => {
  loadingStates.value[examDate] = true;
  errorStates.value[examDate] = false;
  
  try {
    const response = await getActiveGroupCount(props.course.name, examDate) as ActiveGroupsResponse;
    loadedGroups.value[examDate] = response.groups || [];
  } catch (error) {
    console.error(`Error loading groups for ${examDate}:`, error);
    errorStates.value[examDate] = true;
  } finally {
    loadingStates.value[examDate] = false;
  }
};
</script>
