import { betterAuth } from "better-auth";
import { Pool, PoolConfig } from "pg";

const poolConfig: PoolConfig = {
  host: process.env.PGSQL_HOST!,
  port: parseInt(process.env.PGSQL_PORT!),
  user: process.env.PGSQL_USER!,
  password: process.env.PGSQL_PASS!,
  database: process.env.PGSQL_DB_NAME!,
};

const pool = new Pool(poolConfig);

export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
  // secret:
  //   process.env.BETTER_AUTH_SECRET || "your-secret-key-at-least-32-chars-long",
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});

export const getSession = auth.api.getSession;
export const signUp = auth.api.signUpEmail;
export const signIn = auth.api.signInEmail;
export const signOut = auth.api.signOut;
