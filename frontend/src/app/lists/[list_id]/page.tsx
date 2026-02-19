"use client";

import { useParams } from "next/navigation";
import { useList } from "@/features/lists/hooks/use-lists";
import { BreadcrumbNav } from "@/features/lists/components/breadcrumb";
import { ListActionButtons } from "@/features/lists/components/list-action-buttons";
import { EditableName } from "@/features/lists/components/editable-name";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";
import { Loader2, Plus } from "lucide-react";
import { useState } from "react";

function LoadingState() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
    </div>
  );
}

function NotFoundState() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
      <h1 className="text-4xl font-bold mb-2">404</h1>
      <p className="text-xl text-muted-foreground mb-6">List not found</p>
      <Button asChild>
        <Link href="/dashboard">Return to Dashboard</Link>
      </Button>
    </div>
  );
}

function ForbiddenState() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
      <h1 className="text-4xl font-bold mb-2">403</h1>
      <p className="text-xl text-muted-foreground mb-6">You don&apos;t have access to this list</p>
      <Button asChild>
        <Link href="/dashboard">Return to Dashboard</Link>
      </Button>
    </div>
  );
}

function EmptyState() {
  return (
    <Card className="mt-8">
      <CardContent className="pt-6 text-center">
        <p className="text-lg text-muted-foreground mb-2">No tasks yet</p>
        <p className="text-sm text-muted-foreground">Add your first task above</p>
      </CardContent>
    </Card>
  );
}

export default function ListDetailPage() {
  const params = useParams();
  const listId = params.list_id ? Number(params.list_id) : null;
  const { data: list, isLoading, error } = useList(listId);
  const [isEditingName, setIsEditingName] = useState(false);

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    const errorMessage = error.message || "";
    if (errorMessage.includes("404")) {
      return <NotFoundState />;
    }
    if (errorMessage.includes("403")) {
      return <ForbiddenState />;
    }
    // Handle other errors
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
        <p className="text-xl text-destructive mb-6">Error: {errorMessage}</p>
        <Button asChild>
          <Link href="/dashboard">Return to Dashboard</Link>
        </Button>
      </div>
    );
  }

  if (!list) {
    return <NotFoundState />;
  }

  const isOwner = true; // For now, if we can access the list, we own it (Epic 4 will add sharing)

  const handleEditClick = () => {
    setIsEditingName(true);
  };

  const handleNameChange = () => {
    setIsEditingName(false);
  };

  return (
    <div className="container mx-auto py-8 max-w-4xl">
      <BreadcrumbNav listName={list.name} />
      
      <div className="flex justify-between items-center mt-6 mb-8">
        <EditableName
          listId={list.id}
          name={list.name}
          isOwner={isOwner}
          isEditing={isEditingName}
          onEditComplete={handleNameChange}
        />
        {isOwner && (
          <ListActionButtons 
            listId={list.id} 
            listName={list.name} 
            onEditClick={handleEditClick}
          />
        )}
      </div>

      {/* Add task input - will be functional in Epic 3 */}
      <div className="flex gap-2 mb-8">
        <Input 
          placeholder="Add your first task" 
          className="flex-1"
          disabled
        />
        <Button disabled>
          <Plus className="h-4 w-4 mr-1" />
          Add
        </Button>
      </div>

      <EmptyState />
    </div>
  );
}
