import {
  CognitoIdentityProviderClient,
  InitiateAuthCommand,
  SignUpCommand,
  ConfirmSignUpCommand,
  ResendConfirmationCodeCommand,
  ForgotPasswordCommand,
  ConfirmForgotPasswordCommand,
  GetUserCommand,
  GlobalSignOutCommand,
} from "@aws-sdk/client-cognito-identity-provider";

// FIXED: Your Cognito configuration
const COGNITO_CONFIG = {
  region: "us-east-1",
  userPoolId: "us-east-1_AAAsvcGJ0",
  clientId: "37knpbcken8qob8acd8vg16l6g",
  userPoolName: "readme-generator-users",
  clientName: "readme-generator-web-client",
};

// FIXED: Initialize Cognito client properly
const cognitoClient = new CognitoIdentityProviderClient({
  region: COGNITO_CONFIG.region,
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
  refreshToken: string;
}

class CognitoAuthService {
  // FIXED: Sign up new user
  async signUp(email: string, password: string, name?: string) {
    try {
      const command = new SignUpCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
        Password: password,
        UserAttributes: [
          {
            Name: "email",
            Value: email,
          },
          ...(name ? [{ Name: "name", Value: name }] : []),
        ],
      });

      const response = await cognitoClient.send(command);
      return {
        success: true,
        userSub: response.UserSub,
        codeDeliveryDetails: response.CodeDeliveryDetails,
      };
    } catch (error: any) {
      console.error("Sign up error:", error);
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Confirm sign up with verification code
  async confirmSignUp(email: string, confirmationCode: string) {
    try {
      const command = new ConfirmSignUpCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
        ConfirmationCode: confirmationCode,
      });

      await cognitoClient.send(command);
      return { success: true };
    } catch (error: any) {
      console.error("Confirmation error:", error);
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Sign in user with correct auth flow
  async signIn(email: string, password: string) {
    try {
      // Use USER_PASSWORD_AUTH (this is the correct enum value)
      const command = new InitiateAuthCommand({
        ClientId: COGNITO_CONFIG.clientId,
        AuthFlow: "USER_PASSWORD_AUTH",
        AuthParameters: {
          USERNAME: email,
          PASSWORD: password,
        },
      });

      const response = await cognitoClient.send(command);

      if (response.AuthenticationResult) {
        const tokens: AuthTokens = {
          accessToken: response.AuthenticationResult.AccessToken!,
          idToken: response.AuthenticationResult.IdToken!,
          refreshToken: response.AuthenticationResult.RefreshToken!,
        };

        // Store tokens securely
        if (typeof window !== 'undefined') {
          localStorage.setItem("cognito_tokens", JSON.stringify(tokens));
          localStorage.setItem("auth_token", tokens.accessToken);
        }

        // Get user info
        const userInfo = await this.getCurrentUser(tokens.accessToken);
        if (userInfo.success && typeof window !== 'undefined') {
          localStorage.setItem("user_data", JSON.stringify(userInfo.user));
        }

        return {
          success: true,
          tokens,
          user: userInfo.user,
        };
      } else {
        return {
          success: false,
          error: "Authentication failed - no tokens received",
        };
      }
    } catch (error: any) {
      console.error("Sign in error:", error);
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Get current user info
  async getCurrentUser(accessToken?: string) {
    try {
      const token = accessToken || (typeof window !== 'undefined' ? localStorage.getItem("auth_token") : null);
      
      if (!token) {
        return {
          success: false,
          error: "No access token available",
        };
      }

      const command = new GetUserCommand({
        AccessToken: token,
      });

      const response = await cognitoClient.send(command);
      
      const user: CognitoUser = {
        sub: response.UserAttributes?.find(attr => attr.Name === 'sub')?.Value || '',
        email: response.UserAttributes?.find(attr => attr.Name === 'email')?.Value || '',
        name: response.UserAttributes?.find(attr => attr.Name === 'name')?.Value,
        given_name: response.UserAttributes?.find(attr => attr.Name === 'given_name')?.Value,
        family_name: response.UserAttributes?.find(attr => attr.Name === 'family_name')?.Value,
        email_verified: response.UserAttributes?.find(attr => attr.Name === 'email_verified')?.Value === 'true',
        preferred_username: response.UserAttributes?.find(attr => attr.Name === 'preferred_username')?.Value,
      };

      return {
        success: true,
        user,
      };
    } catch (error: any) {
      console.error("Get user error:", error);
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Sign out user
  async signOut() {
    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem("auth_token") : null;
      
      if (token) {
        const command = new GlobalSignOutCommand({
          AccessToken: token,
        });
        await cognitoClient.send(command);
      }

      // Clear local storage
      if (typeof window !== 'undefined') {
        localStorage.removeItem("cognito_tokens");
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user_data");
      }

      return { success: true };
    } catch (error: any) {
      console.error("Sign out error:", error);
      // Still clear local storage even if API call fails
      if (typeof window !== 'undefined') {
        localStorage.removeItem("cognito_tokens");
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user_data");
      }
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Resend confirmation code
  async resendConfirmationCode(email: string) {
    try {
      const command = new ResendConfirmationCodeCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
      });

      const response = await cognitoClient.send(command);
      return {
        success: true,
        codeDeliveryDetails: response.CodeDeliveryDetails,
      };
    } catch (error: any) {
      console.error("Resend code error:", error);
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Forgot password
  async forgotPassword(email: string) {
    try {
      const command = new ForgotPasswordCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
      });

      const response = await cognitoClient.send(command);
      return {
        success: true,
        codeDeliveryDetails: response.CodeDeliveryDetails,
      };
    } catch (error: any) {
      console.error("Forgot password error:", error);
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Confirm forgot password
  async confirmForgotPassword(email: string, confirmationCode: string, newPassword: string) {
    try {
      const command = new ConfirmForgotPasswordCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
        ConfirmationCode: confirmationCode,
        Password: newPassword,
      });

      await cognitoClient.send(command);
      return { success: true };
    } catch (error: any) {
      console.error("Confirm forgot password error:", error);
      return {
        success: false,
        error: this.getErrorMessage(error),
      };
    }
  }

  // FIXED: Check if user is authenticated
  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    
    const token = localStorage.getItem("auth_token");
    const userData = localStorage.getItem("user_data");
    
    return !!(token && userData);
  }

  // FIXED: Get stored user data
  getStoredUser(): CognitoUser | null {
    if (typeof window === 'undefined') return null;
    
    const userData = localStorage.getItem("user_data");
    return userData ? JSON.parse(userData) : null;
  }

  // FIXED: Better error message handling
  private getErrorMessage(error: any): string {
    if (error.name === 'UserNotFoundException') {
      return 'User not found. Please check your email or sign up.';
    }
    if (error.name === 'NotAuthorizedException') {
      return 'Invalid email or password.';
    }
    if (error.name === 'UserNotConfirmedException') {
      return 'Please verify your email before signing in.';
    }
    if (error.name === 'CodeMismatchException') {
      return 'Invalid verification code.';
    }
    if (error.name === 'ExpiredCodeException') {
      return 'Verification code has expired. Please request a new one.';
    }
    if (error.name === 'UsernameExistsException') {
      return 'An account with this email already exists.';
    }
    if (error.name === 'InvalidPasswordException') {
      return 'Password does not meet requirements.';
    }
    if (error.name === 'LimitExceededException') {
      return 'Too many attempts. Please try again later.';
    }
    
    return error.message || 'An unexpected error occurred.';
  }
}

// Export singleton instance
export const cognitoAuth = new CognitoAuthService();
export default cognitoAuth;
