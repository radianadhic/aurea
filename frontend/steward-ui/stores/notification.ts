/**
 * Notification Pinia store.
 * Manages toast notifications across the app.
 */
import { defineStore } from 'pinia';
import { ElNotification, ElMessage } from 'element-plus';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

interface Notification {
  id: number;
  type: NotificationType;
  title: string;
  message: string;
  duration: number;
  timestamp: number;
}

interface NotificationState {
  notifications: Notification[];
  nextId: number;
}

export const useNotificationStore = defineStore('notification', {
  state: (): NotificationState => ({
    notifications: [],
    nextId: 1,
  }),

  actions: {
    show(type: NotificationType, message: string, title?: string, duration = 5000) {
      // Show using Element Plus
      switch (type) {
        case 'success':
          ElMessage.success(message);
          break;
        case 'error':
          ElMessage.error(message);
          break;
        case 'warning':
          ElMessage.warning(message);
          break;
        case 'info':
        default:
          ElMessage.info(message);
          break;
      }

      // Track in store
      const notification: Notification = {
        id: this.nextId++,
        type,
        title: title || this.getDefaultTitle(type),
        message,
        duration,
        timestamp: Date.now(),
      };
      this.notifications.unshift(notification);

      // Auto-remove
      setTimeout(() => {
        this.remove(notification.id);
      }, duration);

      // Keep only last 50
      if (this.notifications.length > 50) {
        this.notifications = this.notifications.slice(0, 50);
      }
    },

    showSuccess(message: string, title?: string) {
      this.show('success', message, title);
    },

    showError(message: string, title?: string) {
      this.show('error', message, title);
    },

    showWarning(message: string, title?: string) {
      this.show('warning', message, title);
    },

    showInfo(message: string, title?: string) {
      this.show('info', message, title);
    },

    showDetailed(type: NotificationType, title: string, message: string, duration = 8000) {
      ElNotification({
        title,
        message,
        type,
        duration,
        position: 'top-right',
        dangerouslyUseHTMLString: false,
      });
    },

    remove(id: number) {
      const index = this.notifications.findIndex((n) => n.id === id);
      if (index !== -1) {
        this.notifications.splice(index, 1);
      }
    },

    clear() {
      this.notifications = [];
    },

    getDefaultTitle(type: NotificationType): string {
      const titles: Record<NotificationType, string> = {
        success: 'Berhasil',
        error: 'Error',
        warning: 'Peringatan',
        info: 'Informasi',
      };
      return titles[type];
    },
  },
});
