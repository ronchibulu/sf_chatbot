"use client";

import * as React from "react";
import Link from "next/link";
import { Home, List, LogOut, User } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
  SidebarInset,
} from "@/components/ui/sidebar";
import { SignOutBtn } from "@/features/auth/components/sign-out-btn";

interface AppShellProps {
  children: React.ReactNode;
  session: {
    user?: {
      name?: string | null;
      email?: string | null;
    };
  };
}

function DashboardSidebar({ session }: { session: AppShellProps["session"] }) {
  return (
    <>
      <SidebarHeader className="py-4">
        <div className="flex flex-col gap-1 px-4">
          <span className="text-lg font-semibold">SleekFlow</span>
          <span className="text-xs text-muted-foreground truncate">
            {session.user?.name} | {session.user?.email}
          </span>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild isActive>
              <Link href="/dashboard">
                <Home className="size-4" />
                <span>Dashboard</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild>
              <Link href="/dashboard">
                <User className="size-4" />
                <span>{session.user?.name || "User"}</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SignOutBtn />
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </>
  );
}

export function AppShell({ children, session }: AppShellProps) {
  return (
    <SidebarProvider defaultOpen>
      <div className="flex min-h-screen w-full">
        <Sidebar>
          <DashboardSidebar session={session} />
        </Sidebar>

        <SidebarInset>
          <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
            <SidebarTrigger />
            <div className="flex flex-1 items-center justify-end gap-4">
              <span className="text-sm text-muted-foreground hidden sm:inline">
                {session.user?.name} | {session.user?.email}
              </span>
            </div>
          </header>
          {children}
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
}
