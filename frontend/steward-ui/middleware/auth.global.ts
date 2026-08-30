/**
 * Global auth middleware.
 * Redirects unauthenticated users to login.
 * Restores auth state from storage on first navigation.
 */
import { useAuthStore } from '~/stores/auth';

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();

  // Initialize auth state once
  if (!authStore.initialized) {
    await authStore.restoreFromStorage();
  }

  // Public routes - no auth required
  const publicRoutes = ['/auth/login', '/auth/callback', '/auth/forgot-password', '/auth/reset-password'];
  const isPublic = publicRoutes.some((p) => to.path.startsWith(p));

  // If not authenticated and trying to access protected route
  if (!authStore.isAuthenticated && !isPublic) {
    return navigateTo({
      path: '/auth/login',
      query: { redirect: to.fullPath },
    });
  }

  // If authenticated and on login page, redirect to dashboard
  if (authStore.isAuthenticated && to.path === '/auth/login') {
    return navigateTo('/dashboard');
  }

  // Check role-based access
  const requiredRoles = to.meta.roles as string[] | undefined;
  if (requiredRoles && requiredRoles.length > 0) {
    if (!authStore.hasAnyRole(...requiredRoles)) {
      return navigateTo('/403');
    }
  }

  return undefined;
});
