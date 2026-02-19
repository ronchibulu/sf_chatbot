/** Auth feature types. */
export interface User {
  id: string;
  name: string | null;
  email: string | null;
  image: string | null;
}

export interface AuthError {
  message: string;
  code?: string;
}

export interface SignUpParams {
  email: string;
  password: string;
  name: string;
}

export interface SignInParams {
  email: string;
  password: string;
}
