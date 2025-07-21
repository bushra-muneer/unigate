import { mount } from '@vue/test-utils';
import { describe, expect, it, vi } from 'vitest';

vi.mock('@/composables/useGroups', () => ({
  useGroups: () => ({
    getProfessorsCourses: async () => [
      { id: 1, name: 'Capstone', exams: [{ date: '2025-06-01', groupCount: 2, avgMembers: 5, activeGroupCount: 1 }] },
      { id: 2, name: 'Distributed Systems', exams: [{ date: '2025-07-01', groupCount: 3, avgMembers: 4, activeGroupCount: 2 }] },
    ],
    getGroupCount: async () => ({ count: 2 }),
    getAverageMembers: async () => ({ avg: 5 }),
    getActiveGroupCount: async () => ({ groups: [{ students: ['a', 'b'] }], student_names: ['a', 'b'] }),
    getGroupCreationDistribution: async () => ({ groups_info: [] }),
    getYearlyStats: async () => ({}),
  }),
}));

import Dashboard from '@/pages/dashboard.vue';

const mockCourses = [
  {
    id: 1,
    name: 'Capstone',
    exams: [
      { date: '2025-06-01', groupCount: 2, avgMembers: 5, activeGroupCount: 1 },
    ],
  },
  {
    id: 2,
    name: 'Distributed Systems',
    exams: [
      { date: '2025-07-01', groupCount: 3, avgMembers: 4, activeGroupCount: 2 },
    ],
  },
];

describe('Dashboard.vue integration', () => {
  it('updates widgets when course is changed', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        stubs: {
          CourseCard: {
            template: '<div class="course-card-stub">{{ course.name }}</div>',
            props: ['course'],
          },
          GroupCreationChart: { template: '<div class="group-chart-stub"></div>' },
          ExamDateDropdown: { template: '<div class="exam-date-dropdown-stub"></div>' },
          LoadingIndicator: false,
        },
      },
      data() {
        return {
          courses: mockCourses,
          isLoading: false,
          course: '',
        };
      },
    });

    wrapper.vm.isLoading = false;
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Select a course to view details');

    const input = wrapper.find('input#course_input');
    await input.setValue('Capstone');
    await wrapper.findComponent({ name: 'CourseSearchBox' }).vm.$emit('select', mockCourses[0]);
    await wrapper.vm.$nextTick();

    expect(wrapper.html()).toContain('Capstone');
    expect(wrapper.findAll('.course-card-stub').length).toBe(1);

    await input.setValue('Distributed Systems');
    await wrapper.findComponent({ name: 'CourseSearchBox' }).vm.$emit('select', mockCourses[1]);
    await wrapper.vm.$nextTick();

    expect(wrapper.html()).toContain('Distributed Systems');
    expect(wrapper.findAll('.course-card-stub').length).toBe(1);
    expect(wrapper.html()).not.toContain('Capstone');
  });
}); 