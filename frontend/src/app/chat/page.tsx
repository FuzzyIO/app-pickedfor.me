'use client';

import { useAuth } from '@/hooks/useAuth';
import ChatInterface from '@/components/chat/ChatInterface';
import Link from 'next/link';

export default function ChatPage() {
  const { user, isLoading } = useAuth();

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
          <div className="flex items-center space-x-4">
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
              ← Back to Dashboard
            </Link>
            <h1 className="text-xl font-bold text-gray-900">Trip Planning</h1>
          </div>
          <div className="text-sm text-gray-600">
            {user?.full_name || user?.email}
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto h-[calc(100vh-12rem)]">
          <ChatInterface />
        </div>
      </main>
    </div>
  );
}