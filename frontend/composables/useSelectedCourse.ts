import { ref, watch, computed } from 'vue';

const SELECTED_COURSE_KEY = 'unigate_selected_course';

export function useSelectedCourse(courses) {
  const selectedCourseId = ref('');

  // Sort courses alphabetically by name
  const sortedCourses = computed(() =>
    [...courses.value].sort((a, b) => a.name.localeCompare(b.name))
  );

  function initialize() {
    if (typeof window === 'undefined') return;
    const saved = localStorage.getItem(SELECTED_COURSE_KEY);
    if (saved && courses.value.some(c => c.id === saved)) {
      selectedCourseId.value = saved;
    } else if (courses.value.length) {
      selectedCourseId.value = sortedCourses.value[0].id;
    }
  }

  // Watch for changes and persist
  watch(selectedCourseId, (val) => {
    if (val) localStorage.setItem(SELECTED_COURSE_KEY, val);
  });

  // Re-initialize when courses change
  watch(courses, initialize, { immediate: true });

  return { selectedCourseId };
} 