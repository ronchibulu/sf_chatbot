import { createAuthClient } from "better-auth/react";

export const { signUp, signIn, signOut, useSession } = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});
