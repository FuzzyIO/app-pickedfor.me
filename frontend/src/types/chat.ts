export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
  created_at?: string;
  conversation_id?: string;
  llm_metadata?: Record<string, any>;
  isLoading?: boolean;
  error?: boolean;
}

export interface Conversation {
  id: string;
  user_id: string;
  trip_id?: string;
  messages: Message[];
  state: ConversationState;
  context: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export enum ConversationState {
  INITIAL_INTENT = 'initial_intent',
  GATHERING_CONTEXT = 'gathering_context',
  REFINING_PREFERENCES = 'refining_preferences',
  PRESENTING_OPTIONS = 'presenting_options',
  DEEP_PLANNING = 'deep_planning',
  BOOKING_ASSISTANCE = 'booking_assistance',
}

export interface ConversationContext {
  purpose?: string;
  startDate?: string;
  endDate?: string;
  partySize?: number;
  budget?: {
    min?: number;
    max?: number;
  };
  preferences?: {
    activities?: string[];
    cuisine?: string[];
    accommodation?: string[];
  };
  destinations?: string[];
}

// API request/response types
export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: Message;
  state: ConversationState;
  context: Record<string, any>;
}

export interface ConversationCreate {
  state?: ConversationState;
  context?: Record<string, any>;
  trip_id?: string;
}

export interface ConversationUpdate {
  state?: ConversationState;
  context?: Record<string, any>;
  trip_id?: string;
}