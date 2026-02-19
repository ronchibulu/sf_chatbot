import { redirect } from 'next/navigation';
import { getSession } from '@/lib/auth';
import { LoginForm } from '@/features/auth/components/login-form';
import { headers } from "next/headers";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface LoginPageProps {
  searchParams: Promise<{ message?: string; error?: string }>;
}

export default async function LoginPage(props: LoginPageProps) {
  // Check if user is already logged in - redirect to dashboard
  const session = await getSession({
    headers: await headers()
  });
  
  if (session) {
    redirect('/dashboard');
  }

  const searchParams = await props.searchParams;
  const message = searchParams?.message;
  const errorMessage = searchParams?.error;

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-h2">Welcome Back</CardTitle>
          <CardDescription>Sign in to your TODO list account</CardDescription>
        </CardHeader>
        <CardContent>
          {/* Session expired or please log in message */}
          {(message || errorMessage) && (
            <div className="mb-4 p-3 text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-md">
              {errorMessage === 'session_expired' 
                ? 'Session expired, please log in again'
                : message || 'Please log in to continue'}
            </div>
          )}
          
          <LoginForm />
          
          <p className="mt-6 text-center text-sm text-muted-foreground">
            Don&apos;t have an account?{' '}
            <a href="/register" className="text-primary font-medium hover:underline">
              Sign up
            </a>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
