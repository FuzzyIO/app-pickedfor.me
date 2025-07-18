export interface User {
  id: string;
  email: string;
  full_name: string | null;
  profile_picture: string | null;
  is_active: boolean;
  preferences: Record<string, any>;
  created_at: string;
  last_login: string | null;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}