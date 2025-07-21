import { mount } from '@vue/test-utils';
import { describe, expect, it, vi } from 'vitest';

vi.mock('@/composables/useGroups', () => ({
  useGroups: () => ({
    getCoursesWithGroups: async () => [],
    getGroupMemberCount: async () => 1,
  }),
}));

import CourseGroupsTab from '@/components/professor/CourseGroupsTab.vue';

const mockCoursesWithGroups = [
  {
    courseId: '1',
    courseName: 'Capstone',
    groups: [
      { id: 'g1', name: 'Alpha', status: 'Active', examDate: '2025-06-01', description: 'desc', courseName: 'Capstone', type: 'Public', tags: ['ai'], member_count: 3 },
      { id: 'g2', name: 'Beta', status: 'Inactive', examDate: '2025-07-01', description: 'desc', courseName: 'Capstone', type: 'Private', tags: ['blockchain'], member_count: 2 },
      { id: 'g3', name: 'Gamma', status: 'Active', examDate: '2025-06-01', description: 'desc', courseName: 'Capstone', type: 'Public', tags: ['ml'], member_count: 4 },
      { id: 'g4', name: 'Delta', status: 'Recently Over', examDate: '2025-08-01', description: 'desc', courseName: 'Capstone', type: 'Public', tags: ['ds'], member_count: 1 },
    ],
  },
  {
    courseId: '2',
    courseName: 'Distributed Systems',
    groups: [
      { id: 'g5', name: 'Omega', status: 'Active', examDate: '2025-09-01', description: 'desc', courseName: 'Distributed Systems', type: 'Public', tags: ['net'], member_count: 5 },
    ],
  },
];

describe('CourseGroupsTab.vue Multi-Level Navigation', () => {
  it('expands course, status, and exam date levels, shows correct groups', async () => {
    const wrapper = mount(CourseGroupsTab, {
      global: {
        stubs: {
          GroupCard: { props: ['group'], template: '<div class="group-card-stub">{{ group.name }}</div>' },
        },
      },
      data() {
        return {
          coursesWithGroups: [],
          isLoading: false,
        };
      },
    });
    await wrapper.vm.$nextTick();
    wrapper.vm.coursesWithGroups.splice(0, 0, ...mockCoursesWithGroups);
    await wrapper.vm.$nextTick();
    wrapper.vm.searchQuery = "Capstone";
    await wrapper.vm.$nextTick();
    wrapper.vm.searchQuery = "";
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Capstone');
    expect(wrapper.text()).toContain('Distributed Systems');

    await wrapper.findAll('div.cursor-pointer.font-bold')[0].trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('Active');
    expect(wrapper.text()).toContain('Inactive');
    expect(wrapper.text()).toContain('Recently Over');

    const activeStatus = wrapper.findAll('div.cursor-pointer.font-semibold').find(el => el.text().includes('Active'));
    await activeStatus.trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('Exam Date: 01/06/2025');

    const examDate = wrapper.findAll('div.cursor-pointer.text-sm').find(el => el.text().includes('Exam Date: 01/06/2025'));
    await examDate.trigger('click');
    await wrapper.vm.$nextTick();
    const groupCards = wrapper.findAll('.group-card-stub');
    expect(groupCards.length).toBeGreaterThan(0);
    expect(wrapper.text()).toContain('Alpha');
    expect(wrapper.text()).toContain('Gamma');
  });
}); 