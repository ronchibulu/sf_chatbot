"use client";

import { useState } from "react";
import { todoItemStatusLabel, type TodoItem as TodoItemType } from "../types";
import { Loader2, Trash2, Pencil } from "lucide-react";
import { useDeleteTodoItem, useRestoreTodoItem } from "../hooks/use-todo-items";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { PriorityBadge } from "./priority-badge";
import { DueDateDisplay } from "./due-date-display";
import { MoreOptionsDropdown } from "./more-options-dropdown";
import { TaskModal } from "./task-modal";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface TodoItemProps {
  item: TodoItemType;
  canEdit?: boolean;
  isSelected?: boolean;
  onSelect?: (id: number, selected: boolean) => void;
}

export function TodoItem({
  item,
  canEdit = false,
  isSelected = false,
  onSelect,
}: TodoItemProps) {
  const deleteItem = useDeleteTodoItem();
  const restoreItem = useRestoreTodoItem();
  const { toast } = useToast();
  const [isDeleting, setIsDeleting] = useState(false);
  const [deletedItem, setDeletedItem] = useState<{
    id: number;
    text: string;
  } | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleDelete = async () => {
    if (!canEdit) return;

    setDeletedItem({ id: item.id, text: item.text });
    setIsDeleting(true);

    try {
      await deleteItem.mutateAsync({ itemId: item.id });

      toast({
        title: "Task deleted",
        description: (
          <div className="flex items-center gap-2">
            <span>Task deleted</span>
            <Button
              variant="link"
              size="sm"
              onClick={async (e) => {
                e.preventDefault();
                try {
                  await restoreItem.mutateAsync({ itemId: item.id });
                  toast({
                    title: "Task restored",
                  });
                } catch {
                  toast({
                    title: "Failed to restore",
                    description: "The undo period may have expired",
                    variant: "destructive",
                  });
                }
                setDeletedItem(null);
              }}
            >
              Undo
            </Button>
          </div>
        ),
        duration: 5000,
      });
    } catch (error) {
      setIsDeleting(false);
      setDeletedItem(null);
    }
  };

  return (
    <>
      <Card className="w-full h-full group">
        <CardHeader>
          <div className="flex justify-between mb-2">
            <div>
              <CardTitle className="text-h2">{item.text}</CardTitle>
              {item.description && (
                <CardDescription className="flex flex-col gap-1">
                  {item.description}
                  <div className="gap-2 space-y-1">
                    {item.priority && (
                      <PriorityBadge priority={item.priority} />
                    )}
                  </div>
                </CardDescription>
              )}
            </div>
            <div className="flex space-x-1">
              {canEdit && (
                <Button
                  variant="ghost"
                  size="icon"
                  className="opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8 text-muted-foreground hover:text-primary"
                  onClick={() => setIsModalOpen(true)}
                >
                  <Pencil className="h-4 w-4" />
                </Button>
              )}

              <MoreOptionsDropdown
                item={item}
                currentDueDate={item.due_date?.toString()}
                currentPriority={item.priority}
              />

              {canEdit && (
                <Button
                  variant="ghost"
                  size="icon"
                  className="opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8 text-muted-foreground hover:text-destructive"
                  onClick={handleDelete}
                  disabled={deleteItem.isPending}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex-1 min-w-0">
            {item.due_date && (
              <DueDateDisplay
                dueDate={new Date(item.due_date)}
                isCompleted={item.status === "completed"}
              />
            )}
            {item.created_at}
            {item.updated_at}
            {item.priority}
            <div className="flex items-center gap-2 mt-2 flex-wrap">
              {item.status && (
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                  {todoItemStatusLabel[item.status]}
                </span>
              )}
              {item.tags &&
                item.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700"
                  >
                    {tag}
                  </span>
                ))}
            </div>
          </div>
        </CardContent>
      </Card>

      <TaskModal item={item} open={isModalOpen} onOpenChange={setIsModalOpen} />
    </>
  );
}

interface TodoItemListProps {
  items: TodoItemType[];
  isLoading?: boolean;
  canEdit?: boolean;
  selectedIds?: number[];
  onSelectionChange?: (ids: number[]) => void;
}

export function TodoItemList({
  items,
  isLoading,
  canEdit = false,
  selectedIds = [],
  onSelectionChange,
}: TodoItemListProps) {
  const handleSelect = (id: number, selected: boolean) => {
    if (!onSelectionChange) return;
    if (selected) {
      onSelectionChange([...selectedIds, id]);
    } else {
      onSelectionChange(selectedIds.filter((selectedId) => selectedId !== id));
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (items.length === 0) {
    return null;
  }

  return (
    <div className="grid md:grid-cols-2 gap-4">
      {items.map((item) => (
        <TodoItem
          key={item.id}
          item={item}
          canEdit={canEdit}
          isSelected={selectedIds.includes(item.id)}
          onSelect={handleSelect}
        />
      ))}
    </div>
  );
}
