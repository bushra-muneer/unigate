<script setup lang="ts">
import { VisXYContainer, VisLine, VisAxis, VisScatter } from "@unovis/vue";
import { computed, defineProps } from 'vue';

const props = defineProps<{
  courseId: string | number;
  examDate: string;
  data: Array<{ creation_date: string; count: number; exam_date?: string }>;
  isLoading: boolean;
}>();

function safeParseDate(dateStr: any): number | null {
  if (!dateStr || typeof dateStr !== 'string') return null;
  const parsed = Date.parse(dateStr);
  return isNaN(parsed) ? null : parsed;
}

const chartData = computed(() =>
  (props.data || [])
    .map((item) => {
      const timestamp = safeParseDate(item.creation_date);
      const count = typeof item.count === "number" ? item.count : NaN;
      return { date: timestamp, count };
    })
    .filter((item) => item.date !== null && !isNaN(item.count))
);

const xAccessor = (d: { date: number }) => new Date(d.date);
const yAccessor = (d: { count: number }) => d.count;
</script>

<template>
  <div id="group_creation_chart">
    <div v-if="props.isLoading" class="text-center py-8">Loading chart...</div>
    <VisXYContainer v-else style="width: 100%; height: 300px">
      <VisLine
        v-if="chartData.length > 1"
        :data="chartData"
        :x="xAccessor"
        :y="yAccessor"
        :style="{ stroke: '#0000FF' }"
      />
      <VisScatter
        v-else
        :data="chartData"
        :x="xAccessor"
        :y="yAccessor"
        :style="{ fill: '#0000FF', r: 6 }"
      />
      <VisAxis
        type="x"
        scale="time"
        :tickFormat="(d) => new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })"
      />
      <VisAxis type="y" />
    </VisXYContainer>
  </div>
</template>
