import { create } from 'zustand';
import { Message, Conversation, ConversationState } from '@/types/chat';

interface ChatStore {
  conversations: Conversation[];
  currentConversation: Conversation | null;
  
  // Actions
  createConversation: (userId: string) => Conversation;
  setCurrentConversation: (conversation: Conversation | null) => void;
  addMessage: (conversationId: string, message: Message) => void;
  updateConversationState: (conversationId: string, state: ConversationState) => void;
  updateConversationContext: (conversationId: string, context: any) => void;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  conversations: [],
  currentConversation: null,

  createConversation: (userId: string) => {
    const newConversation: Conversation = {
      id: crypto.randomUUID(),
      userId,
      messages: [],
      state: ConversationState.INITIAL_INTENT,
      context: {},
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    set((state) => ({
      conversations: [...state.conversations, newConversation],
      currentConversation: newConversation,
    }));

    return newConversation;
  },

  setCurrentConversation: (conversation) => {
    set({ currentConversation: conversation });
  },

  addMessage: (conversationId, message) => {
    set((state) => ({
      conversations: state.conversations.map((conv) =>
        conv.id === conversationId
          ? { ...conv, messages: [...conv.messages, message], updatedAt: new Date().toISOString() }
          : conv
      ),
      currentConversation:
        state.currentConversation?.id === conversationId
          ? {
              ...state.currentConversation,
              messages: [...state.currentConversation.messages, message],
              updatedAt: new Date().toISOString(),
            }
          : state.currentConversation,
    }));
  },

  updateConversationState: (conversationId, state) => {
    set((store) => ({
      conversations: store.conversations.map((conv) =>
        conv.id === conversationId
          ? { ...conv, state, updatedAt: new Date().toISOString() }
          : conv
      ),
      currentConversation:
        store.currentConversation?.id === conversationId
          ? { ...store.currentConversation, state, updatedAt: new Date().toISOString() }
          : store.currentConversation,
    }));
  },

  updateConversationContext: (conversationId, context) => {
    set((store) => ({
      conversations: store.conversations.map((conv) =>
        conv.id === conversationId
          ? { ...conv, context: { ...conv.context, ...context }, updatedAt: new Date().toISOString() }
          : conv
      ),
      currentConversation:
        store.currentConversation?.id === conversationId
          ? {
              ...store.currentConversation,
              context: { ...store.currentConversation.context, ...context },
              updatedAt: new Date().toISOString(),
            }
          : store.currentConversation,
    }));
  },
}))