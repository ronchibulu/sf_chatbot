"use client";

import { useParams } from "next/navigation";
import { useList } from "@/features/lists/hooks/use-lists";
import { useTodoItems } from "@/features/todo-items/hooks/use-todo-items";
import { BreadcrumbNav } from "@/features/lists/components/breadcrumb";
import { ListActionButtons } from "@/features/lists/components/list-action-buttons";
import { EditableName } from "@/features/lists/components/editable-name";
import { AddTaskModal } from "@/features/todo-items/components/add-task-modal";
import { TodoItemList } from "@/features/todo-items/components/todo-item";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";
import { Loader2 } from "lucide-react";
import { useEffect, useState } from "react";

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
      <p className="text-xl text-muted-foreground mb-6">
        You don&apos;t have access to this list
      </p>
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
        <p className="text-sm text-muted-foreground">
          Add your first task above
        </p>
      </CardContent>
    </Card>
  );
}

export default function ListDetailPage() {
  const params = useParams();
  const listId = params.list_id ? Number(params.list_id) : null;
  const { data: list, isLoading, error } = useList(listId);
  const { data: items, isLoading: itemsLoading } = useTodoItems(listId);
  const [isEditingName, setIsEditingName] = useState(false);

  useEffect(() => {
    console.log("list Items:", items);
  }, [items]);

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

  const isOwner = true;

  const handleEditClick = () => {
    setIsEditingName(true);
  };

  const handleNameChange = () => {
    setIsEditingName(false);
  };

  return (
    <main className="flex flex-1 flex-col gap-4 p-4">
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
            isOwner={isOwner}
            onEditClick={handleEditClick}
          />
        )}
      </div>

      <div className="mb-6">
        <AddTaskModal listId={list.id} canAdd={isOwner} />
      </div>

      {items && items.length > 0 ? (
        <div className="space-y-4">
          <TodoItemList items={items} canEdit={isOwner} />
        </div>
      ) : (
        <EmptyState />
      )}
    </main>
  );
}
