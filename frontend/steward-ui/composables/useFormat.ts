/**
 * Format composable - common formatters
 */
import dayjs from 'dayjs';
import 'dayjs/locale/id';
import relativeTime from 'dayjs/plugin/relativeTime';
import localizedFormat from 'dayjs/plugin/localizedFormat';

dayjs.extend(relativeTime);
dayjs.extend(localizedFormat);
dayjs.locale('id');

export function useFormat() {
  /**
   * Format number with Indonesian locale
   */
  const formatNumber = (value: number | null | undefined, decimals = 0): string => {
    if (value === null || value === undefined || isNaN(value)) return '-';
    return new Intl.NumberFormat('id-ID', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value);
  };

  /**
   * Format as IDR currency
   */
  const formatCurrency = (amount: number | null | undefined, currency = 'IDR'): string => {
    if (amount === null || amount === undefined || isNaN(amount)) return '-';
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  /**
   * Format date
   */
  const formatDate = (date: string | Date | null | undefined, format = 'DD MMM YYYY'): string => {
    if (!date) return '-';
    return dayjs(date).format(format);
  };

  /**
   * Format datetime
   */
  const formatDateTime = (date: string | Date | null | undefined): string => {
    if (!date) return '-';
    return dayjs(date).format('DD MMM YYYY HH:mm');
  };

  /**
   * Format date relative (e.g., "2 jam yang lalu")
   */
  const formatRelative = (date: string | Date | null | undefined): string => {
    if (!date) return '-';
    return dayjs(date).fromNow();
  };

  /**
   * Format NIK with masking (show last 4)
   */
  const formatNik = (nik: string | null | undefined, mask = true): string => {
    if (!nik) return '-';
    if (mask) {
      const last4 = nik.slice(-4);
      return `************${last4}`;
    }
    return nik;
  };

  /**
   * Format phone with country code
   */
  const formatPhone = (phone: string | null | undefined): string => {
    if (!phone) return '-';
    if (phone.startsWith('+62')) return phone;
    if (phone.startsWith('0')) return '+62' + phone.substring(1);
    return phone;
  };

  /**
   * Get initials from name
   */
  const getInitials = (name: string | null | undefined): string => {
    if (!name) return '?';
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  };

  /**
   * Truncate text
   */
  const truncate = (text: string, maxLength = 50): string => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
  };

  /**
   * Format file size
   */
  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return {
    formatNumber,
    formatCurrency,
    formatDate,
    formatDateTime,
    formatRelative,
    formatNik,
    formatPhone,
    getInitials,
    truncate,
    formatFileSize,
  };
}
