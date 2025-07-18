import React from 'react';
import { Message } from '@/types/chat';

interface MessageItemProps {
  message: Message;
}

export default function MessageItem({ message }: MessageItemProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[70%] rounded-lg p-4 ${
          isUser
            ? 'bg-primary-600 text-white'
            : 'bg-gray-100 text-gray-900'
        } ${message.error ? 'bg-red-100 text-red-700' : ''}`}
      >
        {message.isLoading ? (
          <div className="flex items-center space-x-2">
            <div className="animate-bounce w-2 h-2 bg-gray-500 rounded-full"></div>
            <div className="animate-bounce w-2 h-2 bg-gray-500 rounded-full delay-100"></div>
            <div className="animate-bounce w-2 h-2 bg-gray-500 rounded-full delay-200"></div>
          </div>
        ) : (
          <div className="whitespace-pre-wrap">{message.content}</div>
        )}
        <div
          className={`text-xs mt-2 ${
            isUser ? 'text-primary-200' : 'text-gray-500'
          }`}
        >
          {new Date(message.timestamp || message.created_at || '').toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}