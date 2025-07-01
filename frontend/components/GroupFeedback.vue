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
</style> <template>
  <div v-if="canShowFeedback" class="w-full">
    <div class="bg-white border border-gray-200 rounded-lg p-6">
      <div v-if="!alreadySubmitted">
        <div class="flex justify-center items-center mb-8">
          <div class="flex items-center">
            <template v-for="(step, index) in steps" :key="index">
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center cursor-pointer transition-colors relative"
                :class="[
                  currentStep === index
                    ? 'bg-blue-600 text-white'
                    : isStepCompleted(index)
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-600 hover:bg-gray-300',
                ]"
              >
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
                <span v-else>{{ index + 1 }}</span>
              </div>
              <div
                v-if="index < steps.length - 1"
                class="w-16 h-1"
                :class="[
                  currentStep > index || isStepCompleted(index + 1)
                    ? 'bg-blue-600'
                    : 'bg-gray-200',
                ]"
              ></div>
            </template>
          </div>
        </div>

        <div class="space-y-6">
          <transition name="fade" mode="out-in">
            <div :key="currentStep" class="space-y-4 text-center">
              <h4 class="text-lg font-medium mb-4">{{ steps[currentStep].question }}</h4>
              <div v-if="steps[currentStep].type === 'boolean'" class="flex justify-center gap-8">
                <button @click="handleResponse(steps[currentStep].field, true)" class="text-4xl hover:scale-110 transition-transform" :disabled="isStepCompleted(currentStep)">👍</button>
                <button @click="handleResponse(steps[currentStep].field, false)" class="text-4xl hover:scale-110 transition-transform" :disabled="isStepCompleted(currentStep)">👎</button>
              </div>
              <div v-if="steps[currentStep].type === 'choice'" class="flex flex-col items-center gap-3">
                 <button
                  v-for="option in steps[currentStep].options"
                  :key="option"
                  @click="handleResponse(steps[currentStep].field, option)"
                  class="w-48 px-6 py-3 rounded-lg transition-colors"
                  :disabled="isStepCompleted(currentStep)"
                  :class="[
                    responses[steps[currentStep].field] === option
                      ? 'bg-blue-600 text-white'
                      : isStepCompleted(currentStep)
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-800',
                  ]"
                >
                  {{ option }}
                </button>
              </div>
            </div>
          </transition>
        </div>
      </div>

      <div v-else class="space-y-4">
        <h3 class="text-xl text-center font-semibold text-green-600">
          You Helped a lot! Thanks for your Participation.
        </h3>
        <div class="mt-6 text-left border-t pt-4">
            <h4 class="font-semibold mb-3 text-gray-700">Your submitted answers:</h4>
            <ul class="space-y-2 text-sm text-gray-600">
                <li class="flex justify-between items-center">
                    <span>Was this group helpful?</span>
                    <span class="font-bold">{{ responses.helpful ? '👍 Yes' : '👎 No' }}</span>
                </li>
                <li class="flex justify-between items-center">
                    <span>Did you attend the exam?</span>
                    <span class="font-bold">{{ responses.attended ? '👍 Yes' : '👎 No' }}</span>
                </li>
                <li class="flex justify-between items-center">
                    <span>Which group size works best?</span>
                    <span class="font-bold">{{ responses.bestSize }}</span>
                </li>
            </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from '#imports';
import { useRoute } from 'vue-router';
import { useCurrentStudent } from '~/composables/useCurrentStudent';
import { useFeedback } from '~/composables/useFeedback';
import { useApiFetch } from '~/composables/useApiFetch';

// --- PROPS & ROUTE ---
const props = defineProps<{
  examDate: string;
}>();
const route = useRoute();
const groupId = route.params.id as string;

// --- STATE ---
const steps = [
  { field: 'helpful', question: 'Was this group helpful?', type: 'boolean' as const },
  { field: 'attended', question: 'Did you attend the exam in this exam date?', type: 'boolean' as const },
  { field: 'bestSize', question: 'Which group size do you think works best?', type: 'choice' as const, options: ['2–5', '6–10', '11–20', '21–5'] }
];
const currentStep = ref(0);
const responses = ref({
  helpful: null as boolean | null,
  attended: null as boolean | null,
  bestSize: null as string | null,
});
const alreadySubmitted = ref(false);

// --- COMPOSABLES ---
const { currentStudent, getCurrentStudent } = useCurrentStudent();
const { saveAnswer } = useFeedback();

// --- COMPUTED PROPERTIES ---
const canShowFeedback = computed(() => {
  if (!props.examDate) return false;
  const examDate = new Date(props.examDate);
  const today = new Date();
  return examDate < today;
});

// --- LIFECYCLE HOOKS ---
onMounted(async () => {
  await getCurrentStudent();
  if (!currentStudent.value || !groupId) return;

  try {
    const { data: existingResponses } = await useApiFetch(
      `/feedback/responses?student_id=${currentStudent.value.id}&group_id=${groupId}`
    );
    
    // Эта проверка - ключевая. Она смотрит на ответ от сервера.
    if (existingResponses.value && existingResponses.value.length > 0) {
      // 1. Ставим флаг, что студент уже отвечал
      alreadySubmitted.value = true;
      
      // 2. Заполняем локальные данные ответами с сервера для их отображения
      for (const resp of existingResponses.value) {
        const field = resp.question_id as keyof typeof responses.value;
        if (field in responses.value) {
          let value: string | boolean = resp.answer;
          if (steps.find(s => s.field === field)?.type === 'boolean') {
            value = (resp.answer === 'true');
          }
          (responses.value[field] as any) = value;
        }
      }
    }
  } catch (error) {
    console.error('Error fetching existing feedback:', error);
  }
});

// --- METHODS ---
const isStepCompleted = (stepIndex: number) => {
  const step = steps[stepIndex];
  if (!step) return false;
  const field = step.field as keyof typeof responses.value;
  return responses.value[field] !== null;
};

const handleResponse = async (
  field: keyof typeof responses.value,
  value: boolean | string
) => {
  if (isStepCompleted(currentStep.value)) return;

  (responses.value[field] as boolean | string | null) = value;

  if (!currentStudent.value) {
    await getCurrentStudent();
    if (!currentStudent.value) return;
  }
  
  const payload = {
    student_id: currentStudent.value.id,
    group_id: groupId,
    question_id: field,
    answer: String(value),
    exam_date: props.examDate,
  };

  try {
    await saveAnswer(payload);
  } catch (err) {
    console.error('Failed to save answer:', err);
    (responses.value[field] as any) = null;
    return;
  }

  if (currentStep.value < steps.length - 1) {
    setTimeout(() => {
      currentStep.value++;
    }, 300);
  } else {
    alreadySubmitted.value = true;
  }
};
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