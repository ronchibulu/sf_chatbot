import { redirect } from 'next/navigation';
import { getSession } from '@/lib/auth';
import { RegisterForm } from '@/features/auth/components/register-form';
import { headers } from "next/headers";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default async function RegisterPage() {
  // Check if user is already logged in - redirect to dashboard
  const session = await getSession({
    headers: await headers()
  });
  
  if (session) {
    redirect('/dashboard');
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-h2">Create Account</CardTitle>
          <CardDescription>Sign up for your TODO list account</CardDescription>
        </CardHeader>
        <CardContent>
          <RegisterForm />
          
          <p className="mt-6 text-center text-sm text-muted-foreground">
            Already have an account?{' '}
            <a href="/login" className="text-primary font-medium hover:underline">
              Sign in
            </a>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
