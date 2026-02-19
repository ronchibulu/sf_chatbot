"use client";

import { useAuth } from "../hooks/use-auth";
import { Button } from "@/components/ui/button";

export function SignOutBtn() {
  const { signOut } = useAuth();

  return (
    <Button onClick={() => signOut()} variant="outline" size="sm">
      Sign Out
    </Button>
  );
}
