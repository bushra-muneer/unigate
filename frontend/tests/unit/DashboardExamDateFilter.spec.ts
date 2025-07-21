import { mount } from '@vue/test-utils';
import { describe, expect, it, vi } from 'vitest';

// Мокаем useGroups, чтобы не было зависимости от Nuxt useState
vi.mock('@/composables/useGroups', () => ({
  useGroups: () => ({
    getProfessorsCourses: async () => [
      {
        id: 1,
        name: 'Capstone',
        exams: [
          { date: '2025-06-01', groupCount: 2, avgMembers: 5, activeGroupCount: 1 },
          { date: '2025-07-01', groupCount: 3, avgMembers: 4, activeGroupCount: 2 },
        ],
      },
    ],
    getGroupCount: async () => ({ count: 2 }),
    getAverageMembers: async () => ({ avg: 5 }),
    getActiveGroupCount: async (course, date) => {
      if (date === '2025-06-01') {
        return { groups: [{ students: ['a', 'b'] }], student_names: ['a', 'b'] };
      }
      if (date === '2025-07-01') {
        return { groups: [{ students: ['c'] }], student_names: ['c'] };
      }
      // No data for other dates
      return { groups: [], student_names: [] };
    },
    getGroupCreationDistribution: async (course) => {
      if (course === 'Capstone') {
        return {
          groups_info: [
            { creation_date: '2025-06-01T10:00:00Z' },
            { creation_date: '2025-07-01T10:00:00Z' },
          ],
        };
      }
      return { groups_info: [] };
    },
    getYearlyStats: async () => ({
      2025: { totalGroups: 5, totalMembers: 10 },
    }),
  }),
}));

import Dashboard from '@/pages/dashboard.vue';

describe('Dashboard.vue exam date filter', () => {
  it('updates widgets when a new exam date is selected', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          CourseCard: { template: '<div class="course-card-stub">{{ course.name }}</div>', props: ['course'] },
          GroupCreationChart: { template: '<div class="group-chart-stub"></div>' },
          ExamDateDropdown: { template: '<select><option>All</option><option>2025-06-01</option><option>2025-07-01</option></select>' },
          LoadingIndicator: false,
        },
      },
    });

    // Отключаем лоадер
    wrapper.vm.isLoading = false;
    await wrapper.vm.$nextTick();

    // Выбираем курс
    const input = wrapper.find('input#course_input');
    await input.setValue('Capstone');
    await wrapper.findComponent({ name: 'CourseSearchBox' }).vm.$emit('select', {
      id: 1,
      name: 'Capstone',
      exams: [
        { date: '2025-06-01', groupCount: 2, avgMembers: 5, activeGroupCount: 1 },
        { date: '2025-07-01', groupCount: 3, avgMembers: 4, activeGroupCount: 2 },
      ],
    });
    await wrapper.vm.$nextTick();

    // По умолчанию examDate пустой, виджеты должны показывать все данные (All)
    expect(wrapper.html()).toContain('Capstone');

    // Выбираем конкретную дату
    wrapper.vm.examDate = '2025-06-01';
    await wrapper.vm.$nextTick();
    // Проверяем, что данные соответствуют только этой дате (например, student_names = ['a', 'b'])
    expect(wrapper.vm.studentNames).toEqual(['a', 'b']);

    // Выбираем другую дату
    wrapper.vm.examDate = '2025-07-01';
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.studentNames).toEqual(['c']);

    // Выбираем дату, для которой нет данных
    wrapper.vm.examDate = '2025-08-01';
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.studentNames).toEqual([]);
    // Можно проверить, что отображается fallback/empty state (например, текст "No data" или отсутствие виджетов)
  });
}); 