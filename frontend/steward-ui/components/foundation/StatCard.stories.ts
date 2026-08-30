import type { Meta, StoryObj } from '@storybook/vue3';
import StatCard from './StatCard.vue';

const meta = {
  title: 'Foundation/StatCard',
  component: StatCard,
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
  argTypes: {
    label: { control: 'text' },
    value: { control: 'text' },
    unit: { control: 'text' },
    icon: { control: 'text' },
    color: { control: 'color' },
    trend: { control: { type: 'range', min: -100, max: 100, step: 0.1 } },
    subValue: { control: 'text' },
  },
} satisfies Meta<typeof StatCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: 'Total Nasabah',
    value: 1245872,
    icon: '👥',
    color: '#1e40af',
    trend: 8.2,
    trendPeriod: 'vs bulan lalu',
    subValue: '1,187,203 aktif',
  },
};

export const KYC: Story = {
  args: {
    label: 'KYC Pending',
    value: 234,
    icon: '📋',
    color: '#d97706',
    trend: -12.5,
    trendPeriod: 'vs minggu lalu',
  },
};

export const NoTrend: Story = {
  args: {
    label: 'Match Queue',
    value: 89,
    icon: '🔄',
    color: '#0284c7',
  },
};
