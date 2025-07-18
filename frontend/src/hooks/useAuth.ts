import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';

export const useAuth = (requireAuth = true) => {
  const router = useRouter();
  const { user, token, isLoading, isAuthenticated, fetchUser } = useAuthStore();

  useEffect(() => {
    if (token && !user && !isLoading) {
      fetchUser();
    }
  }, [token, user, isLoading, fetchUser]);

  useEffect(() => {
    if (!isLoading && requireAuth && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, requireAuth, isAuthenticated, router]);

  return {
    user,
    isLoading,
    isAuthenticated,
  };
};