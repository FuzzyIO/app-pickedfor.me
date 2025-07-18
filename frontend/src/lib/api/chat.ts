import { api } from '../api';
import { 
  Conversation, 
  Message, 
  ChatRequest, 
  ChatResponse,
  ConversationCreate,
  ConversationUpdate 
} from '@/types/chat';

export const chatApi = {
  // List all conversations
  listConversations: async (): Promise<Conversation[]> => {
    const { data } = await api.get('/chat/conversations');
    return data;
  },

  // Get a specific conversation with messages
  getConversation: async (conversationId: string): Promise<Conversation> => {
    const { data } = await api.get(`/chat/conversations/${conversationId}`);
    return data;
  },

  // Create a new conversation
  createConversation: async (data: ConversationCreate): Promise<Conversation> => {
    const { data: conversation } = await api.post('/chat/conversations', data);
    return conversation;
  },

  // Update a conversation
  updateConversation: async (
    conversationId: string, 
    data: ConversationUpdate
  ): Promise<Conversation> => {
    const { data: conversation } = await api.patch(
      `/chat/conversations/${conversationId}`, 
      data
    );
    return conversation;
  },

  // Delete a conversation
  deleteConversation: async (conversationId: string): Promise<void> => {
    await api.delete(`/chat/conversations/${conversationId}`);
  },

  // Send a chat message
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const { data } = await api.post('/chat/chat', request);
    return data;
  },
};