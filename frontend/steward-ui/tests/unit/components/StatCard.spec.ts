import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import StatCard from '~/components/foundation/StatCard.vue';

describe('StatCard.vue', () => {
  it('renders value and label', () => {
    const wrapper = mount(StatCard, {
      props: {
        label: 'Total Customers',
        value: 1000,
      },
    });
    expect(wrapper.text()).toContain('Total Customers');
    expect(wrapper.text()).toContain('1000');
  });

  it('renders with icon', () => {
    const wrapper = mount(StatCard, {
      props: {
        label: 'KYC Pending',
        value: 234,
        icon: '📋',
      },
    });
    expect(wrapper.text()).toContain('📋');
  });

  it('shows trend up for positive', () => {
    const wrapper = mount(StatCard, {
      props: {
        label: 'Growth',
        value: 1000,
        trend: 8.2,
      },
    });
    expect(wrapper.find('.stat-trend.up').exists()).toBe(true);
  });

  it('shows trend down for negative', () => {
    const wrapper = mount(StatCard, {
      props: {
        label: 'Decline',
        value: 1000,
        trend: -12.5,
      },
    });
    expect(wrapper.find('.stat-trend.down').exists()).toBe(true);
  });

  it('renders unit', () => {
    const wrapper = mount(StatCard, {
      props: {
        label: 'Amount',
        value: 1500,
        unit: 'IDR',
      },
    });
    expect(wrapper.text()).toContain('IDR');
  });
});
