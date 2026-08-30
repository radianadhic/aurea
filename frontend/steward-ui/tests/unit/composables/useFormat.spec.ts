import { describe, it, expect } from 'vitest';
import { useFormat } from '~/composables/useFormat';

describe('useFormat composable', () => {
  const { formatNumber, formatCurrency, formatDate, formatNik, formatPhone, getInitials, truncate } = useFormat();

  describe('formatNumber', () => {
    it('formats numbers with Indonesian locale', () => {
      expect(formatNumber(1234567)).toMatch(/1\.234\.567/);
    });

    it('returns dash for null/undefined', () => {
      expect(formatNumber(null)).toBe('-');
      expect(formatNumber(undefined)).toBe('-');
    });

    it('respects decimals option', () => {
      expect(formatNumber(1234.5, 2)).toMatch(/1\.234,50/);
    });
  });

  describe('formatCurrency', () => {
    it('formats as IDR', () => {
      const result = formatCurrency(1500000);
      expect(result).toContain('1.500.000');
      expect(result).toMatch(/Rp|IDR/);
    });

    it('handles zero', () => {
      const result = formatCurrency(0);
      expect(result).toContain('0');
    });
  });

  describe('formatDate', () => {
    it('formats ISO date string', () => {
      expect(formatDate('2026-01-26')).toMatch(/26 Jan 2026/);
    });

    it('returns dash for null', () => {
      expect(formatDate(null)).toBe('-');
    });
  });

  describe('formatNik', () => {
    it('masks NIK by default', () => {
      const masked = formatNik('3201234567890001');
      expect(masked).toBe('************0001');
    });

    it('returns full NIK when mask=false', () => {
      const full = formatNik('3201234567890001', false);
      expect(full).toBe('3201234567890001');
    });
  });

  describe('formatPhone', () => {
    it('prepends +62 to local format', () => {
      expect(formatPhone('081234567890')).toBe('+6281234567890');
    });

    it('keeps +62 format as is', () => {
      expect(formatPhone('+6281234567890')).toBe('+6281234567890');
    });
  });

  describe('getInitials', () => {
    it('returns 2 chars for full name', () => {
      expect(getInitials('Budi Santoso')).toBe('BS');
    });

    it('returns 2 chars for single name', () => {
      expect(getInitials('Budi')).toBe('BU');
    });

    it('returns ? for empty', () => {
      expect(getInitials('')).toBe('?');
    });
  });

  describe('truncate', () => {
    it('truncates long text', () => {
      expect(truncate('This is a long text that should be truncated', 20)).toBe('This is a long ...');
    });

    it('keeps short text as is', () => {
      expect(truncate('Short', 20)).toBe('Short');
    });
  });
});
