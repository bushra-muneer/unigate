import ProfessorHome from '@/pages/ProfessorHome.vue';
import { mount } from '@vue/test-utils';
import { describe, expect, it, vi } from 'vitest';
import { createMemoryHistory, createRouter } from 'vue-router';

const routes = [
  { path: '/professor/home', name: 'ProfessorHome', component: ProfessorHome },
];

const mountWithRouter = async (initialQuery = {}) => {
  const router = createRouter({
    history: createMemoryHistory(),
    routes,
  });
  router.replace = vi.fn();
  await router.push({ name: 'ProfessorHome', query: initialQuery });
  await router.isReady();
  return { wrapper: mount(ProfessorHome, {
    global: {
      plugins: [router],
      stubs: {
        TabSwitcher: {
          template: `<div><button id="tab-dashboard" @click="$emit('update:modelValue', 'dashboard')">Dashboard</button><button id="tab-groups" @click="$emit('update:modelValue', 'groups')">Course Groups</button></div>`
        },
        DashboardTab: { template: '<div class="dashboard-tab">Dashboard Content</div>' },
        CourseGroupsTab: { template: '<div class="groups-tab">Groups Content</div>' },
      },
    },
  }), router };
};

describe('ProfessorHome.vue Tab Switching', () => {
  it('default is Dashboard tab', async () => {
    const { wrapper } = await mountWithRouter();
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('Dashboard Content');
    expect(wrapper.find('.dashboard-tab').exists()).toBe(true);
    expect(wrapper.find('.groups-tab').exists()).toBe(false);
  });

  it('clicking Course Groups tab switches content and updates tab', async () => {
    const { wrapper } = await mountWithRouter();
    await wrapper.vm.$nextTick();
    await wrapper.find('#tab-groups').trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('Groups Content');
    expect(wrapper.find('.groups-tab').exists()).toBe(true);
    expect(wrapper.find('.dashboard-tab').exists()).toBe(false);
  });

  it('clicking Dashboard tab switches back', async () => {
    const { wrapper } = await mountWithRouter({ tab: 'groups' });
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('Groups Content');
    await wrapper.find('#tab-dashboard').trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.text()).toContain('Dashboard Content');
    expect(wrapper.find('.dashboard-tab').exists()).toBe(true);
  });

  it('URL query updates on tab switch', async () => {
    const { wrapper, router } = await mountWithRouter();
    await wrapper.vm.$nextTick();
    expect(router.replace).toHaveBeenCalledWith({ query: { tab: 'dashboard' } });
  });
}); 