"use client";

import { useState } from "react";
import { Plus, List } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { SignOutBtn } from "@/features/auth/components/sign-out-btn";
import { CreateListModal } from "@/features/lists/components/create-list-modal";
import { useLists } from "@/features/lists/hooks/use-lists";
import Link from "next/link";

interface DashboardClientProps {
  session: {
    user?: {
      name?: string | null;
      email?: string | null;
    };
  };
}

export function DashboardClient({ session }: DashboardClientProps) {
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const { data: lists, isLoading } = useLists();

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-card border-b border-border shadow-sm">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-h1 text-foreground">Dashboard</h1>
            <div className="flex items-center gap-4">
              <span className="text-muted-foreground text-sm">
                {session.user?.name} | {session.user?.email}
              </span>
              <SignOutBtn />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-h2 text-foreground">Your TODO Lists</h2>
            <Button onClick={() => setCreateModalOpen(true)}>
              <Plus className="size-4" />
              New List
            </Button>
          </div>

          {isLoading ? (
            <Card>
              <CardContent className="py-8">
                <p className="text-center text-muted-foreground">
                  Loading your lists...
                </p>
              </CardContent>
            </Card>
          ) : lists && lists.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {lists.map((list) => (
                <Link href={`/lists/${list.id}`} key={list.id}>
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer">
                    <CardHeader>
                      <CardTitle className="text-h3">{list.name}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-small text-muted-foreground">
                        Created {new Date(list.createdAt).toLocaleDateString()}
                      </p>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="py-12">
                <div className="text-center">
                  <List className="size-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground mb-4">
                    No TODO lists yet. Start by creating your first list!
                  </p>
                  <Button onClick={() => setCreateModalOpen(true)}>
                    <Plus className="size-4" />
                    Create Your First List
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </main>

      <CreateListModal
        open={createModalOpen}
        onOpenChange={setCreateModalOpen}
      />
    </div>
  );
}
