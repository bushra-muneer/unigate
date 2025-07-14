<script setup lang="ts">
import { defineProps, defineEmits, ref, watch } from 'vue';

const props = defineProps({
  courses: {
    type: Array as () => Array<{ id: number|string, name: string }>,
    required: true,
  },
  modelValue: {
    type: [String, Number],
    default: '',
  },
});

const emit = defineEmits(['update:modelValue']);
const localSelected = ref(props.modelValue);

watch(() => props.modelValue, (val) => {
  localSelected.value = val;
});

watch(localSelected, (val) => {
  emit('update:modelValue', val);
});
</script>

<template>
  <div>
    <label for="courseDropdown" class="block mb-2 text-sm font-medium text-gray-700">
      Course Name
    </label>
    <select
      id="courseDropdown"
      v-model="localSelected"
      class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
    >
      <option v-for="course in courses" :key="course.id" :value="course.id">
        {{ course.name }}
      </option>
    </select>
  </div>
</template> 