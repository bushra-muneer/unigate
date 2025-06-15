<template>
  <div v-if="canShowFeedback" class="w-full">
    <!-- Container with border instead of shadow -->
    <div class="bg-white border border-gray-200 rounded-lg p-6">
      <!-- Stepper Navigation -->
      <div class="flex justify-center items-center mb-8">
        <div class="flex items-center">
          <template v-for="(step, index) in steps" :key="index">
            <!-- Step Circle -->
            <div
              @click="currentStep = index"
              class="w-8 h-8 rounded-full flex items-center justify-center cursor-pointer transition-colors relative"
              :class="[
                currentStep === index
                  ? 'bg-blue-600 text-white'
                  : isStepCompleted(index)
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
              ]"
            >
              <!-- Checkmark for completed steps -->
              <svg
                v-if="isStepCompleted(index)"
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"
                />
              </svg>
              <!-- Step number for incomplete/current steps -->
              <span v-else>{{ index + 1 }}</span>
            </div>
            <!-- Connector Line -->
            <div
              v-if="index < steps.length - 1"
              class="w-16 h-1"
              :class="[
                currentStep > index || isStepCompleted(index + 1)
                  ? 'bg-blue-600'
                  : 'bg-gray-200'
              ]"
            ></div>
          </template>
        </div>
      </div>

      <!-- Question Content -->
      <div class="space-y-6">
        <transition name="fade" mode="out-in">
          <div v-if="currentStep === 0" class="space-y-4 text-center">
            <h4 class="text-lg font-medium mb-4">Was this group helpful?</h4>
            <div class="flex justify-center gap-8">
              <button
                @click="handleResponse('helpful', true)"
                class="text-4xl hover:scale-110 transition-transform"
                :class="{ 'opacity-50': responses.helpful === false }"
              >
                👍
              </button>
              <button
                @click="handleResponse('helpful', false)"
                class="text-4xl hover:scale-110 transition-transform"
                :class="{ 'opacity-50': responses.helpful === true }"
              >
                👎
              </button>
            </div>
          </div>

          <div v-else-if="currentStep === 1" class="space-y-4 text-center">
            <h4 class="text-lg font-medium mb-4">Did you attend the exam in this exam date?</h4>
            <div class="flex justify-center gap-8">
              <button
                @click="handleResponse('attended', true)"
                class="text-4xl hover:scale-110 transition-transform"
                :class="{ 'opacity-50': responses.attended === false }"
              >
                👍
              </button>
              <button
                @click="handleResponse('attended', false)"
                class="text-4xl hover:scale-110 transition-transform"
                :class="{ 'opacity-50': responses.attended === true }"
              >
                👎
              </button>
            </div>
          </div>

          <div v-else class="space-y-4 text-center">
            <h4 class="text-lg font-medium mb-4">Which group size do you think works best?</h4>
            <div class="flex flex-col items-center gap-3">
              <button
                v-for="size in groupSizes"
                :key="size"
                @click="handleResponse('bestSize', size)"
                class="w-48 px-6 py-3 rounded-lg transition-colors"
                :class="[
                  responses.bestSize === size
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-800'
                ]"
              >
                {{ size }}
              </button>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from '#imports'

const props = defineProps<{
  examDate: string // Expected format: "YYYY-MM-DD"
}>()

const steps = ['Helpful', 'Attended', 'Size']
const currentStep = ref(0)
const groupSizes = ['2–5', '6–10', '11–20', '21–50']

const responses = ref({
  helpful: null as boolean | null,
  attended: null as boolean | null,
  bestSize: null as string | null
})

// Check if the exam date has passed
const canShowFeedback = computed(() => {
  if (!props.examDate) return false
  const examDate = new Date(props.examDate)
  const today = new Date()
  return examDate < today
})

// Check if a step is completed
const isStepCompleted = (step: number) => {
  switch (step) {
    case 0:
      return responses.value.helpful !== null
    case 1:
      return responses.value.attended !== null
    case 2:
      return responses.value.bestSize !== null
    default:
      return false
  }
}

// Handle response and auto-advance
const handleResponse = (field: 'helpful' | 'attended' | 'bestSize', value: boolean | string) => {
  responses.value[field] = value
  // Auto-advance to next question if not on last step
  if (currentStep.value < steps.length - 1) {
    setTimeout(() => {
      currentStep.value++
    }, 300) // Small delay for better UX
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 