"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createTodoItemAction, getTodoItemsAction } from "../api/todo-items";
import { updateTodoItemAction } from "../api/update-todo-item";
import {
  deleteTodoItemAction,
  restoreTodoItemAction,
} from "../api/delete-todo-item";
import { useToast } from "@/components/ui/use-toast";
import { TodoItemStatus, UpdateTodoItem } from "../types";

export function useCreateTodoItem() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({
      listId,
      text,
      description,
      tags,
      status,
    }: {
      listId: number;
      text: string;
      description?: string;
      tags?: string[];
      status: TodoItemStatus;
    }) => createTodoItemAction(listId, { text, description, tags, status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todoItems"] });
      toast({
        title: "Task added successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to add task",
        description:
          error.message || "An error occurred while adding the task.",
        variant: "destructive",
      });
    },
  });
}

export function useUpdateTodoItem() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (updatedData: UpdateTodoItem) =>
      updateTodoItemAction(updatedData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todoItems"] });
      toast({
        title: "Task updated successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to update task",
        description:
          error.message || "An error occurred while updating the task.",
        variant: "destructive",
      });
    },
  });
}

export function useTodoItems(listId: number | null) {
  return useQuery({
    queryKey: ["todoItems", listId],
    queryFn: () => getTodoItemsAction(listId!),
    enabled: !!listId,
  });
}

export function useDeleteTodoItem() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ itemId }: { itemId: number }) =>
      deleteTodoItemAction(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todoItems"] });
      toast({
        title: "Task deleted",
        duration: 5000,
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to delete task",
        description:
          error.message || "An error occurred while deleting the task.",
        variant: "destructive",
      });
    },
  });
}

export function useRestoreTodoItem() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ itemId }: { itemId: number }) =>
      restoreTodoItemAction(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todoItems"] });
      toast({
        title: "Task restored",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to restore task",
        description:
          error.message || "An error occurred while restoring the task.",
        variant: "destructive",
      });
    },
  });
}
