/** Auth hooks for BetterAuth integration. */
"use client";

import {
  signUp as betterAuthSignUp,
  signIn as betterAuthSignIn,
  signOut as betterAuthSignOut,
  useSession,
} from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useCallback, useState } from "react";
import type { SignUpParams, SignInParams } from "../types";

export function useAuth() {
  const router = useRouter();
  const { data: session, isPending: isLoading } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const signUp = useCallback(
    async (params: SignUpParams) => {
      setIsSubmitting(true);
      setError(null);

      try {
        const result = await betterAuthSignUp.email({
          email: params.email,
          password: params.password,
          name: params.name,
        });

        if (result.error) {
          setError(result.error.message || "Registration failed");
          return {
            success: false,
            error: result.error.message || "Registration failed",
          };
        }

        // Success - redirect to dashboard
        router.push("/dashboard");
        return { success: true, data: result.data };
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Registration failed";
        setError(message);
        return { success: false, error: message };
      } finally {
        setIsSubmitting(false);
      }
    },
    [router],
  );

  const signIn = useCallback(
    async (params: SignInParams) => {
      setIsSubmitting(true);
      setError(null);

      try {
        const result = await betterAuthSignIn.email({
          email: params.email,
          password: params.password,
        });

        if (result.error) {
          // Generic error message for security - don't reveal if email exists
          const errorMessage = "Invalid email or password";
          setError(errorMessage);
          return {
            success: false,
            error: errorMessage,
          };
        }

        // Success - redirect to dashboard
        router.push("/dashboard");
        return { success: true, data: result.data };
      } catch {
        // Generic error message for security
        const errorMessage = "Invalid email or password";
        setError(errorMessage);
        return { success: false, error: errorMessage };
      } finally {
        setIsSubmitting(false);
      }
    },
    [router],
  );

  const signOut = useCallback(async () => {
    try {
      console.log("signing out");
      const result = await betterAuthSignOut();
      console.log("signOut result:", result);
      
      // Always redirect after signout attempt
      router.push("/login");
    } catch (err) {
      console.error("Sign out failed:", err);
      // Still redirect even on error
      router.push("/login");
    }
  }, [router]);

  return {
    session,
    isLoading,
    isAuthenticated: !!session?.user,
    error,
    isSubmitting,
    signUp,
    signIn,
    signOut,
  };
}
