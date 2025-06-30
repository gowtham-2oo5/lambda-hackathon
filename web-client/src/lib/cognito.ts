// Dynamic AWS SDK imports to avoid build-time issues
let CognitoIdentityProviderClient: any,
  InitiateAuthCommand: any,
  SignUpCommand: any,
  ConfirmSignUpCommand: any,
  ResendConfirmationCodeCommand: any,
  ForgotPasswordCommand: any,
  ConfirmForgotPasswordCommand: any,
  GetUserCommand: any,
  GlobalSignOutCommand: any;
const initializeAWS = async () => {
  if (!CognitoIdentityProviderClient) {
    const awsSdk = await import("@aws-sdk/client-cognito-identity-provider");
    CognitoIdentityProviderClient = awsSdk.CognitoIdentityProviderClient;
    InitiateAuthCommand = awsSdk.InitiateAuthCommand;
    SignUpCommand = awsSdk.SignUpCommand;
    ConfirmSignUpCommand = awsSdk.ConfirmSignUpCommand;
    ResendConfirmationCodeCommand = awsSdk.ResendConfirmationCodeCommand;
    ForgotPasswordCommand = awsSdk.ForgotPasswordCommand;
    ConfirmForgotPasswordCommand = awsSdk.ConfirmForgotPasswordCommand;
    GetUserCommand = awsSdk.GetUserCommand;
    GlobalSignOutCommand = awsSdk.GlobalSignOutCommand;
  }
};

// Your Cognito configuration from AWS scan
const COGNITO_CONFIG = {
  region: "us-east-1",
  userPoolId: "us-east-1_AAAsvcGJ0",
  clientId: "37knpbcken8qob8acd8vg16l6g",
  userPoolName: "readme-generator-users",
  clientName: "readme-generator-web-client",
};

// Initialize Cognito client dynamically
let cognitoClient: any;

const initializeCognitoClient = async () => {
  if (!cognitoClient) {
    await initializeAWS();
    cognitoClient = new CognitoIdentityProviderClient({
      region: COGNITO_CONFIG.region,
    });
  }
  return cognitoClient;
};

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
  // Sign up new user
  async signUp(email: string, password: string, name?: string) {
    try {
      const client = await initializeCognitoClient();
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

      const response = await client.send(command);
      return {
        success: true,
        userSub: response.UserSub,
        codeDeliveryDetails: response.CodeDeliveryDetails,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || "Sign up failed",
      };
    }
  }

  // Confirm sign up with verification code
  async confirmSignUp(email: string, confirmationCode: string) {
    try {
      const client = await initializeCognitoClient();
      const command = new ConfirmSignUpCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
        ConfirmationCode: confirmationCode,
      });

      await client.send(command);
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || "Confirmation failed",
      };
    }
  }

  // Sign in user
  async signIn(email: string, password: string) {
    try {
      const client = await initializeCognitoClient();
      // Use ADMIN_NO_SRP_AUTH flow instead of USER_SRP_AUTH to avoid SRP complexity
      const command = new InitiateAuthCommand({
        ClientId: COGNITO_CONFIG.clientId,
        AuthFlow: "USER_PASSWORD_AUTH",
        AuthParameters: {
          USERNAME: email,
          PASSWORD: password,
        },
      });

      const response = await client.send(command);

      if (response.AuthenticationResult) {
        const tokens: AuthTokens = {
          accessToken: response.AuthenticationResult.AccessToken!,
          idToken: response.AuthenticationResult.IdToken!,
          refreshToken: response.AuthenticationResult.RefreshToken!,
        };

        // Store tokens in localStorage
        localStorage.setItem("cognito_tokens", JSON.stringify(tokens));
        localStorage.setItem("auth_token", tokens.accessToken);

        // Get user info
        const userInfo = await this.getCurrentUser();
        if (userInfo.success) {
          localStorage.setItem("user_data", JSON.stringify(userInfo.user));
        }

        return {
          success: true,
          tokens,
          user: userInfo.success ? userInfo.user : null,
        };
      }

      return {
        success: false,
        error: "Authentication failed",
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || "Sign in failed",
      };
    }
  }

  // Get current user info
  async getCurrentUser(): Promise<{
    success: boolean;
    user?: CognitoUser;
    error?: string;
  }> {
    try {
      const tokens = this.getStoredTokens();
      if (!tokens) {
        return { success: false, error: "No tokens found" };
      }

      const client = await initializeCognitoClient();
      const command = new GetUserCommand({
        AccessToken: tokens.accessToken,
      });

      const response = await client.send(command);

      const user: CognitoUser = {
        sub: response.Username!,
        email: this.getAttribute(response.UserAttributes, "email") || "",
        name: this.getAttribute(response.UserAttributes, "name"),
        given_name: this.getAttribute(response.UserAttributes, "given_name"),
        family_name: this.getAttribute(response.UserAttributes, "family_name"),
        email_verified:
          this.getAttribute(response.UserAttributes, "email_verified") ===
          "true",
        preferred_username: this.getAttribute(
          response.UserAttributes,
          "preferred_username"
        ),
      };

      return { success: true, user };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || "Failed to get user info",
      };
    }
  }

  // Sign out user
  async signOut() {
    try {
      const tokens = this.getStoredTokens();
      if (tokens) {
        const client = await initializeCognitoClient();
        const command = new GlobalSignOutCommand({
          AccessToken: tokens.accessToken,
        });
        await client.send(command);
      }
    } catch (error) {
      console.error("Sign out error:", error);
    } finally {
      // Clear local storage regardless of API call success
      localStorage.removeItem("cognito_tokens");
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user_data");
    }
  }

  // Forgot password
  async forgotPassword(email: string) {
    try {
      const client = await initializeCognitoClient();
      const command = new ForgotPasswordCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
      });

      const response = await client.send(command);
      return {
        success: true,
        codeDeliveryDetails: response.CodeDeliveryDetails,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || "Failed to send reset code",
      };
    }
  }

  // Confirm forgot password
  async confirmForgotPassword(
    email: string,
    confirmationCode: string,
    newPassword: string
  ) {
    try {
      const client = await initializeCognitoClient();
      const command = new ConfirmForgotPasswordCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
        ConfirmationCode: confirmationCode,
        Password: newPassword,
      });

      await client.send(command);
      return { success: true };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || "Failed to reset password",
      };
    }
  }

  // Resend confirmation code
  async resendConfirmationCode(email: string) {
    try {
      const client = await initializeCognitoClient();
      const command = new ResendConfirmationCodeCommand({
        ClientId: COGNITO_CONFIG.clientId,
        Username: email,
      });

      const response = await client.send(command);
      return {
        success: true,
        codeDeliveryDetails: response.CodeDeliveryDetails,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || "Failed to resend code",
      };
    }
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    const tokens = this.getStoredTokens();
    if (!tokens?.accessToken) return false;

    try {
      // Basic JWT token validation (check if not expired)
      const payload = JSON.parse(atob(tokens.accessToken.split(".")[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch {
      return false;
    }
  }

  // Get stored tokens
  private getStoredTokens(): AuthTokens | null {
    try {
      const tokens = localStorage.getItem("cognito_tokens");
      return tokens ? JSON.parse(tokens) : null;
    } catch {
      return null;
    }
  }

  // Helper to get attribute value
  private getAttribute(attributes: any[] | undefined, name: string): string {
    return attributes?.find((attr) => attr.Name === name)?.Value;
  }

  // Get Cognito configuration (for debugging)
  getConfig() {
    return COGNITO_CONFIG;
  }
}

export const cognitoAuth = new CognitoAuthService();
export default cognitoAuth;
