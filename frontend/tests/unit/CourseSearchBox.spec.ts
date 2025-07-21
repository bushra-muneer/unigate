import CourseSearchBox from '@/components/CourseSearchBox.vue';
import { mount } from '@vue/test-utils';
import { describe, expect, it } from 'vitest';

const courses = [
  { name: 'Capstone' },
  { name: 'Distributed Systems' },
  { name: 'Machine Learning' },
];

describe('CourseSearchBox.vue', () => {
  it('shows dropdown and filters courses by input', async () => {
    const wrapper = mount(CourseSearchBox, {
      props: {
        items: courses,
        modelValue: '',
      },
    });
    const input = wrapper.find('input');
    await input.setValue('cap');
    expect(wrapper.vm.filteredItems.length).toBe(1);
    expect(wrapper.html()).toContain('Capstone');
  });

  it('emits select and update:modelValue on course selection', async () => {
    const wrapper = mount(CourseSearchBox, {
      props: {
        items: courses,
        modelValue: '',
      },
    });
    const input = wrapper.find('input');
    await input.setValue('machine');
    // Открыть dropdown и кликнуть по первому элементу
    await wrapper.find('li').trigger('click');
    // Проверяем, что сработал select и update:modelValue
    expect(wrapper.emitted('select')).toBeTruthy();
    expect(wrapper.emitted('update:modelValue')).toBeTruthy();
    // Последнее значение должно быть 'Machine Learning'
    const lastValue = wrapper.emitted('update:modelValue').pop()[0];
    expect(lastValue).toBe('Machine Learning');
  });

  it('updates input and emits on re-selection', async () => {
    const wrapper = mount(CourseSearchBox, {
      props: {
        items: courses,
        modelValue: '',
      },
    });
    const input = wrapper.find('input');
    // Выбрать сначала первый курс
    await input.setValue('cap');
    await wrapper.find('li').trigger('click');
    expect(wrapper.emitted('update:modelValue').pop()[0]).toBe('Capstone');
    // Теперь выбрать другой курс
    await input.setValue('dist');
    await wrapper.find('li').trigger('click');
    expect(wrapper.emitted('update:modelValue').pop()[0]).toBe('Distributed Systems');
  });
}); 