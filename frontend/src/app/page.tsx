'use client';

import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';

export default function Home() {
  const { user, isLoading, isAuthenticated } = useAuth(false);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            Welcome to PickedFor.me
          </h1>
          <p className="text-2xl text-gray-700 mb-12">
            Your AI-powered travel planning assistant
          </p>

          {isLoading ? (
            <div className="animate-pulse">
              <div className="h-12 bg-gray-300 rounded w-48 mx-auto"></div>
            </div>
          ) : isAuthenticated ? (
            <div className="space-y-4">
              <p className="text-lg text-gray-700">
                Welcome back, {user?.full_name || user?.email}!
              </p>
              <Link
                href="/dashboard"
                className="inline-block bg-primary-600 text-white px-8 py-3 rounded-lg hover:bg-primary-700 transition"
              >
                Go to Dashboard
              </Link>
            </div>
          ) : (
            <Link
              href="/login"
              className="inline-block bg-primary-600 text-white px-8 py-3 rounded-lg hover:bg-primary-700 transition"
            >
              Get Started
            </Link>
          )}
        </div>

        <div className="mt-20 grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Smart Recommendations</h3>
            <p className="text-gray-600">
              AI understands your preferences to suggest perfect destinations
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Flexible Planning</h3>
            <p className="text-gray-600">
              Choose what you love, swap what you don't, and keep backups ready
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3">Real-time Adaptation</h3>
            <p className="text-gray-600">
              Automatic adjustments for weather, closures, and conditions
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}