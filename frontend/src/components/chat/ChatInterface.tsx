import React, { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import StarterPrompts from './StarterPrompts';
import { Message, ChatRequest } from '@/types/chat';
import { chatApi } from '@/lib/api/chat';
import { useAuthStore } from '@/store/authStore';

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const { user } = useAuthStore();

  const addMessage = (role: Message['role'], content: string) => {
    const newMessage: Message = {
      id: uuidv4(),
      role,
      content,
      timestamp: new Date().toISOString(),
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newMessage]);
    return newMessage;
  };

  const addLoadingMessage = () => {
    const loadingMessage: Message = {
      id: uuidv4(),
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
      created_at: new Date().toISOString(),
      isLoading: true,
    };
    setMessages((prev) => [...prev, loadingMessage]);
    return loadingMessage.id;
  };

  const updateMessage = (id: string, updates: Partial<Message>) => {
    setMessages((prev) =>
      prev.map((msg) => (msg.id === id ? { ...msg, ...updates } : msg))
    );
  };

  const removeMessage = (id: string) => {
    setMessages((prev) => prev.filter((msg) => msg.id !== id));
  };

  const handleSendMessage = async (content: string) => {
    if (!user) return;

    // Add user message
    addMessage('user', content);
    
    // Add loading message
    const loadingId = addLoadingMessage();
    setIsLoading(true);

    try {
      const chatRequest: ChatRequest = {
        message: content,
        conversation_id: conversationId || undefined
      };
      
      const response = await chatApi.sendMessage(chatRequest);
      
      // Remove loading message
      removeMessage(loadingId);
      
      // Set conversation ID if this was the first message
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }
      
      // Add assistant response
      const assistantMessage: Message = {
        id: response.message.id,
        role: response.message.role,
        content: response.message.content,
        timestamp: response.message.created_at || new Date().toISOString(),
        created_at: response.message.created_at
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      removeMessage(loadingId);
      addMessage(
        'assistant',
        'Sorry, I encountered an error. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      <div className="border-b px-4 py-3">
        <h2 className="text-lg font-semibold text-gray-900">
          AI Travel Assistant
        </h2>
        <p className="text-sm text-gray-500">
          Tell me about your dream trip!
        </p>
      </div>
      
      {messages.length === 0 ? (
        <StarterPrompts onSelectPrompt={handleSendMessage} />
      ) : (
        <MessageList messages={messages} />
      )}
      
      <ChatInput
        onSendMessage={handleSendMessage}
        disabled={isLoading || !user}
        placeholder={
          !user
            ? "Please sign in to start planning"
            : "Tell me about your ideal trip..."
        }
      />
    </div>
  );
}