export interface User {
  id: string;
  email: string;
  name: string;
  plan: "free" | "pro" | "enterprise";
  createdAt?: string;
  avatar?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface SignupCredentials {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  refreshToken?: string;
}

export interface AuthError {
  message: string;
  code?: string;
  field?: string;
}
