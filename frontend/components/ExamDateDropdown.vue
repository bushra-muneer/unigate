<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from "vue";

const props = defineProps({
  dates: {
    type: Array as () => string[],
    required: true,
  },
  modelValue: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:modelValue"]);

// Local state for selected date
const localSelectedDate = ref(props.modelValue);

// Watch for prop changes and update local state
watch(
  () => props.modelValue,
  (newVal) => {
    localSelectedDate.value = newVal;
  },
);

// Emit selected date when it changes
watch(localSelectedDate, (newVal) => {
  emit("update:modelValue", newVal);
});
</script>

<template>
  <div>
    <label for="examDate" class="block mb-2 text-sm font-medium text-gray-700">
      Exam Date
    </label>
    <select
      id="examDate"
      v-model="localSelectedDate"
      class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:border-blue-500"
      :disabled="disabled"
    >
      <option
        v-for="(date, index) in dates"
        :id="'data_' + index"
        :key="date"
        :value="date"
      >
        {{ date }}
      </option>
    </select>
  </div>
</template>
