import GroupCard from '@/components/GroupCard.vue';
import { mount } from '@vue/test-utils';
import { describe, expect, it, vi } from 'vitest';

const push = vi.fn();
vi.mock('vue-router', () => ({
  useRouter: () => ({ push }),
}));

const group = {
  id: '123',
  name: 'Test Group',
  type: 'Private',
  description: 'A test group for students',
  exam_date: '2025-06-01',
  course_name: 'Algorithms',
  members_count: 5,
  tags: ['tag1', 'tag2'],
};

describe('GroupCard.vue (Student)', () => {
  it('renders group info correctly', () => {
    const wrapper = mount(GroupCard, {
      props: { group },
    });
    expect(wrapper.text()).toContain('Test Group');
    expect(wrapper.text()).toContain('A test group for students');
    expect(wrapper.text()).toContain('5');
    expect(wrapper.text()).toContain('01/06/2025');
    expect(wrapper.text()).toContain('tag1');
  });

  it('redirects to group page on click', async () => {
    const wrapper = mount(GroupCard, {
      props: { group },
    });
    await wrapper.trigger('click');
    expect(push).toHaveBeenCalledWith('/groups/123');
  });
}); 