import type {
  LoginCredentials,
  SignupCredentials,
  AuthResponse,
  User,
} from "@/types/auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api";

class AuthAPI {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;

    const config: RequestInit = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    const token = localStorage.getItem("auth_token");
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }

    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response
        .json()
        .catch(() => ({ message: "Network error" }));
      throw new Error(error.message || "Request failed");
    }

    return response.json();
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    // Mock implementation - replace with real API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Simulate login validation
    if (
      credentials.email === "demo@smartreadmegen.com" &&
      credentials.password === "demo123456"
    ) {
      const mockResponse: AuthResponse = {
        user: {
          id: "1",
          email: credentials.email,
          name: credentials.email.split("@")[0],
          plan: "free",
          createdAt: new Date().toISOString(),
        },
        token: "mock_jwt_token_" + Date.now(),
      };
      return mockResponse;
    }

    throw new Error("Invalid credentials");
  }

  async signup(credentials: SignupCredentials): Promise<AuthResponse> {
    // Mock implementation - replace with real API call
    await new Promise((resolve) => setTimeout(resolve, 2000));

    const mockResponse: AuthResponse = {
      user: {
        id: Date.now().toString(),
        email: credentials.email,
        name: credentials.name,
        plan: "free",
        createdAt: new Date().toISOString(),
      },
      token: "mock_jwt_token_" + Date.now(),
    };

    return mockResponse;
  }

  async logout(): Promise<void> {
    // Mock implementation - replace with real API call
    await new Promise((resolve) => setTimeout(resolve, 500));
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user_data");
  }

  async getCurrentUser(): Promise<User> {
    const userData = localStorage.getItem("user_data");
    if (!userData) {
      throw new Error("No user data found");
    }
    return JSON.parse(userData);
  }

  async refreshToken(): Promise<AuthResponse> {
    // Mock implementation - replace with real API call
    const currentUser = await this.getCurrentUser();
    return {
      user: currentUser,
      token: "refreshed_token_" + Date.now(),
    };
  }
}

export const authAPI = new AuthAPI();
