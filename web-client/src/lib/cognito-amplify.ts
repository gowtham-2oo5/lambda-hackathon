import { Amplify } from 'aws-amplify';
import {
  signUp,
  confirmSignUp,
  signIn,
  signOut,
  getCurrentUser,
  fetchAuthSession,
  resendSignUpCode,
  resetPassword,
  confirmResetPassword,
} from 'aws-amplify/auth';

// Configure Amplify with your Cognito settings
Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: 'us-east-1_AAAsvcGJ0',
      userPoolClientId: '37knpbcken8qob8acd8vg16l6g',
      loginWith: {
        email: true,
      },
      signUpVerificationMethod: 'code',
      userAttributes: {
        email: {
          required: true,
        },
        name: {
          required: false,
        },
      },
      allowGuestAccess: false,
      passwordFormat: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireNumbers: true,
        requireSpecialCharacters: true,
      },
    } as any,
  },
});

export interface CognitoUser {
  sub: string;
  email: string;
  name?: string;
  given_name?: string;
  family_name?: string;
  email_verified: boolean;
  preferred_username?: string;
}

export interface AuthTokens {
  accessToken: string;
  idToken: string;
  refreshToken?: string;
}

class AmplifyAuthService {
  // Sign up new user
  async signUp(email: string, password: string, name?: string) {
    try {
      const { isSignUpComplete, userId, nextStep } = await signUp({
        username: email,
        password,
        options: {
          userAttributes: {
            email,
            ...(name && { name }),
          },
        },
      });

      return {
        success: true,
        isSignUpComplete,
        userId,
        nextStep,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Sign up failed',
      };
    }
  }

  // Confirm sign up with verification code
  async confirmSignUp(email: string, confirmationCode: string) {
    try {
      const { isSignUpComplete, nextStep } = await confirmSignUp({
        username: email,
        confirmationCode,
      });

      return {
        success: true,
        isSignUpComplete,
        nextStep,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Confirmation failed',
      };
    }
  }

  // Sign in user
  async signIn(email: string, password: string) {
    try {
      const { isSignedIn, nextStep } = await signIn({
        username: email,
        password,
      });

      if (isSignedIn) {
        // Get user info and tokens
        const [userInfo, session] = await Promise.all([
          this.getCurrentUser(),
          this.getSession(),
        ]);

        // Store tokens in localStorage for compatibility
        if (session.success && session.tokens) {
          localStorage.setItem('cognito_tokens', JSON.stringify(session.tokens));
          localStorage.setItem('auth_token', session.tokens.accessToken);
        }

        if (userInfo.success) {
          localStorage.setItem('user_data', JSON.stringify(userInfo.user));
        }

        return {
          success: true,
          isSignedIn,
          tokens: session.success ? session.tokens : null,
          user: userInfo.success ? userInfo.user : null,
        };
      }

      return {
        success: false,
        error: 'Authentication failed',
        nextStep,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Sign in failed',
      };
    }
  }

  // Get current user info
  async getCurrentUser(): Promise<{ success: boolean; user?: CognitoUser; error?: string }> {
    try {
      const { username, userId } = await getCurrentUser();
      
      // Get user attributes from the session
      const session = await fetchAuthSession();
      const idToken = session.tokens?.idToken;
      
      if (idToken && typeof idToken === 'object' && 'payload' in idToken) {
        const payload = idToken.payload as any;
        
        const user: CognitoUser = {
          sub: userId || username,
          email: payload.email || '',
          name: payload.name,
          given_name: payload.given_name,
          family_name: payload.family_name,
          email_verified: payload.email_verified === true,
          preferred_username: payload.preferred_username,
        };

        return { success: true, user };
      }

      // Fallback if we can't get detailed info
      const user: CognitoUser = {
        sub: userId || username,
        email: username, // Assuming username is email
        email_verified: false,
      };

      return { success: true, user };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Failed to get user info',
      };
    }
  }

  // Get current session and tokens
  async getSession(): Promise<{ success: boolean; tokens?: AuthTokens; error?: string }> {
    try {
      const session = await fetchAuthSession();
      
      if (session.tokens) {
        const tokens: AuthTokens = {
          accessToken: session.tokens.accessToken?.toString() || '',
          idToken: session.tokens.idToken?.toString() || '',
          refreshToken: (session.tokens as any).refreshToken?.toString(),
        };

        return { success: true, tokens };
      }

      return { success: false, error: 'No tokens found' };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Failed to get session',
      };
    }
  }

  // Sign out user
  async signOut() {
    try {
      await signOut();
    } catch (error) {
      console.error('Sign out error:', error);
    } finally {
      // Clear local storage regardless of API call success
      localStorage.removeItem('cognito_tokens');
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_data');
    }
  }

  // Forgot password
  async forgotPassword(email: string) {
    try {
      const output = await resetPassword({ username: email });
      
      return {
        success: true,
        nextStep: output.nextStep,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Failed to send reset code',
      };
    }
  }

  // Confirm forgot password
  async confirmForgotPassword(email: string, confirmationCode: string, newPassword: string) {
    try {
      await confirmResetPassword({
        username: email,
        confirmationCode,
        newPassword,
      });

      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Failed to reset password',
      };
    }
  }

  // Resend confirmation code
  async resendConfirmationCode(email: string) {
    try {
      const output = await resendSignUpCode({ username: email });
      
      return {
        success: true,
        nextStep: (output as any).nextStep,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Failed to resend code',
      };
    }
  }

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    try {
      const session = await fetchAuthSession();
      return !!session.tokens?.accessToken;
    } catch {
      return false;
    }
  }

  // Get stored tokens (for compatibility)
  getStoredTokens(): AuthTokens | null {
    try {
      const tokens = localStorage.getItem('cognito_tokens');
      return tokens ? JSON.parse(tokens) : null;
    } catch {
      return null;
    }
  }
}

export const amplifyAuth = new AmplifyAuthService();
export default amplifyAuth;
