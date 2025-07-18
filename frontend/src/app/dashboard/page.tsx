'use client';

import { useAuth } from '@/hooks/useAuth';
import { useAuthStore } from '@/store/authStore';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, isLoading } = useAuth();
  const { logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">PickedFor.me</h1>
          <div className="flex items-center gap-4">
            {user?.profile_picture && (
              <Image
                src={user.profile_picture}
                alt={user.full_name || 'Profile'}
                width={40}
                height={40}
                className="rounded-full"
              />
            )}
            <span className="text-gray-700">{user?.full_name || user?.email}</span>
            <button
              onClick={handleLogout}
              className="text-gray-600 hover:text-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">
            Welcome to your travel dashboard!
          </h2>

          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h3 className="text-xl font-semibold mb-4">Start Planning Your Trip</h3>
            <p className="text-gray-600 mb-4">
              Tell me about your next adventure and I'll help you plan the perfect trip.
            </p>
            <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition">
              Start New Trip
            </button>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-3">Recent Trips</h3>
              <p className="text-gray-500">No trips yet. Start planning your first adventure!</p>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold mb-3">Your Preferences</h3>
              <p className="text-gray-500">We'll learn your preferences as you plan more trips.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}