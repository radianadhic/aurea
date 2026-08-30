/**
 * Utility functions used across the app.
 */

export function formatNumber(num, decimals = 0) {
  if (num == null) return '-';
  return new Intl.NumberFormat('id-ID', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num);
}

export function formatCurrency(amount, currency = 'IDR') {
  if (amount == null) return '-';
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
  }).format(amount);
}

export function formatDate(date, withTime = true) {
  if (!date) return '-';
  const d = new Date(date);
  const options = {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    timeZone: 'Asia/Jakarta',
  };
  if (withTime) {
    options.hour = '2-digit';
    options.minute = '2-digit';
    options.second = '2-digit';
  }
  return d.toLocaleString('id-ID', options);
}

export function formatRelativeTime(date) {
  if (!date) return '-';
  const now = Date.now();
  const then = new Date(date).getTime();
  const diffSec = Math.floor((now - then) / 1000);

  if (diffSec < 60) return `${diffSec} detik yang lalu`;
  if (diffSec < 3600) return `${Math.floor(diffSec / 60)} menit yang lalu`;
  if (diffSec < 86400) return `${Math.floor(diffSec / 3600)} jam yang lalu`;
  if (diffSec < 2592000) return `${Math.floor(diffSec / 86400)} hari yang lalu`;
  return formatDate(date, false);
}

export function debounce(fn, wait = 300) {
  let timer;
  return function debounced(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), wait);
  };
}

export function copyToClipboard(text) {
  if (navigator.clipboard) {
    return navigator.clipboard.writeText(text);
  }
  // Fallback
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand('copy');
  } finally {
    document.body.removeChild(textarea);
  }
}

export function downloadAsFile(content, filename, mimeType = 'application/json') {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function getInitials(name) {
  if (!name) return '?';
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

export function getStatusColor(status) {
  const colors = {
    UP: 'success',
    DOWN: 'error',
    WARNING: 'warning',
    HEALTHY: 'success',
    DEGRADED: 'warning',
    FAILED: 'error',
    ACTIVE: 'success',
    INACTIVE: 'gray',
    PENDING: 'warning',
    APPROVED: 'success',
    REJECTED: 'error',
    ACT: 'success',
    BLK: 'error',
    DOR: 'warning',
    CLS: 'gray',
  };
  return colors[status] || 'gray';
}

export function toast(message, type = 'info', duration = 3000) {
  window.dispatchEvent(
    new CustomEvent('toast:show', { detail: { message, type, duration } })
  );
}

export default {
  formatNumber,
  formatCurrency,
  formatDate,
  formatRelativeTime,
  debounce,
  copyToClipboard,
  downloadAsFile,
  getInitials,
  getStatusColor,
  toast,
};
