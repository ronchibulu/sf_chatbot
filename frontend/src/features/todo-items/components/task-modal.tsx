"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useUpdateTodoItem } from "../hooks/use-todo-items";
import { Loader2 } from "lucide-react";
import { todoItemStatusValues, type TodoItem } from "../types";

const taskSchema = z.object({
  text: z
    .string()
    .min(1, "Task name is required")
    .max(500, "Task must be 500 characters or less"),
  description: z
    .string()
    .max(2000, "Description must be 2000 characters or less")
    .optional(),
  tags: z.string().optional(),
  status: z.enum(todoItemStatusValues),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface TaskModalProps {
  item: TodoItem;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function TaskModal({ item, open, onOpenChange }: TaskModalProps) {
  const [tagsError, setTagsError] = useState("");
  const updateItem = useUpdateTodoItem();

  const form = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      text: item.text,
      description: item.description || "",
      tags: item.tags?.join(", ") || "",
      status: item.status,
    },
  });

  const resetForm = () => {
    form.reset({
      text: item.text,
      description: item.description || "",
      tags: item.tags?.join(", ") || "",
      status: item.status,
    });
    setTagsError("");
  };

  const handleOpenChange = (isOpen: boolean) => {
    onOpenChange(isOpen);
    if (isOpen) {
      resetForm();
    }
  };

  const handleSubmit = async (data: TaskFormData) => {
    let tags: string[] | undefined;
    if (data.tags) {
      tags = data.tags
        .split(",")
        .map((tag) => tag.trim())
        .filter((tag) => tag.length > 0);
      if (tags.length === 0) {
        setTagsError("Invalid tags format");
        return;
      }
    }

    try {
      await updateItem.mutateAsync({
        list_id: item.list_id,
        id: item.id,
        text: data.text.trim(),
        description: data.description?.trim() || undefined,
        tags,
        status: data.status,
      });
      onOpenChange(false);
    } catch (err) {
      // Error is handled by the mutation
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Edit Task</DialogTitle>
          <DialogDescription>Update the task details below.</DialogDescription>
        </DialogHeader>
        <form onSubmit={form.handleSubmit(handleSubmit)}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="text">Task Name *</Label>
              <Input
                id="text"
                {...form.register("text")}
                placeholder="Enter task name"
                disabled={updateItem.isPending}
              />
              {form.formState.errors.text && (
                <p className="text-sm text-red-500">
                  {form.formState.errors.text.message}
                </p>
              )}
            </div>

            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Input
                id="description"
                {...form.register("description")}
                placeholder="Enter task description (optional)"
                disabled={updateItem.isPending}
              />
              {form.formState.errors.description && (
                <p className="text-sm text-red-500">
                  {form.formState.errors.description.message}
                </p>
              )}
            </div>

            <div className="grid gap-2">
              <Label htmlFor="tags">Tags</Label>
              <Input
                id="tags"
                {...form.register("tags")}
                placeholder="Enter tags separated by commas (optional)"
                disabled={updateItem.isPending}
              />
              {tagsError && <p className="text-sm text-red-500">{tagsError}</p>}
              <p className="text-xs text-muted-foreground">
                Example: work, important, urgent
              </p>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="status">Status</Label>
              <select
                id="status"
                {...form.register("status")}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                disabled={updateItem.isPending}
              >
                <option value="not_started">Not Started</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={updateItem.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={updateItem.isPending}>
              {updateItem.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                "Save Changes"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
