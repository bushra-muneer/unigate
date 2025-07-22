<script setup lang="ts">
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

// Define props
const props = defineProps<{
  data: {
    group_size: string;
    helpful_pct: number;
    not_helpful_pct: number;
    not_answered_pct: number;
  }[];
}>();

const chartData = {
  labels: props.data.map(d => d.group_size),
  datasets: [
    {
      label: 'Helpful',
      data: props.data.map(d => d.helpful_pct),
      backgroundColor: '#4ade80'
    },
    {
      label: 'Not Helpful',
      data: props.data.map(d => d.not_helpful_pct),
      backgroundColor: '#f87171'
    },
    {
      label: 'Not Answered',
      data: props.data.map(d => d.not_answered_pct),
      backgroundColor: '#cbd5e1'
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      ticks: {
        callback: (value: number) => `${value}%`
      }
    }
  }
};
</script>

<template>
  <div style="height: 400px;">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
