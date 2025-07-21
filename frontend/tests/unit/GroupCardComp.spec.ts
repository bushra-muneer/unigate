import GroupCardComp from '@/components/professor/GroupCardComp.vue';
import { mount } from '@vue/test-utils';
import { describe, expect, it } from 'vitest';

describe('GroupCardComp.vue (Professor)', () => {
  const group = {
    id: '456',
    name: 'Prof Group',
    type: 'Public',
    description: 'Professor side group',
    examDate: '2025-07-01',
    courseName: 'Databases',
    member_count: 10,
    tags: ['alpha', 'beta', 'gamma', 'delta'],
  };

  it('renders group info and up to 3 tags', () => {
    const wrapper = mount(GroupCardComp, {
      props: { group },
    });
    expect(wrapper.text()).toContain('Prof Group');
    expect(wrapper.text()).toContain('Professor side group');
    expect(wrapper.text()).toContain('10');
    expect(wrapper.text()).toContain('01/07/2025');
    expect(wrapper.text()).toContain('alpha');
    expect(wrapper.text()).toContain('beta');
    expect(wrapper.text()).toContain('gamma');
    expect(wrapper.text()).not.toContain('delta');
  });

  it('shows courseName if no tags', () => {
    const groupNoTags = { ...group, tags: [] };
    const wrapper = mount(GroupCardComp, {
      props: { group: groupNoTags },
    });
    expect(wrapper.text()).toContain('Databases');
  });

  it('does not throw on click', async () => {
    const wrapper = mount(GroupCardComp, {
      props: { group },
    });
    await expect(wrapper.trigger('click')).resolves.not.toThrow();
  });
}); 