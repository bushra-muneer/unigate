<template>
  <div class="border-b border-gray-200 mb-6">
    <nav class="flex space-x-6 pl-4">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="$emit('update:modelValue', tab.key)"
        :class="[
          'relative inline-flex items-end pb-2 pt-4 text-base font-medium transition-colors duration-200',
            modelValue === tab.key
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 hover:text-blue-600'
        ]"
      >
        {{ tab.label }}
      </button>
    </nav>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  tabs: { key: string; label: string }[];
  modelValue: string;
}>();
defineEmits(['update:modelValue']);
</script>
