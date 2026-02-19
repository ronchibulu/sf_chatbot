"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createListAction, getListsAction, getListAction } from "../api/lists";
import { updateListNameAction } from "../api/update-list-name";
import { deleteListAction } from "../api/delete-list";
import { useToast } from "@/components/ui/use-toast";

export function useCreateList() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: createListAction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["lists"] });
      toast({
        title: "List created successfully",
        description: "Your new TODO list has been created.",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to create list",
        description: error.message || "An error occurred while creating the list.",
        variant: "destructive",
      });
    },
  });
}

export function useLists() {
  return useQuery({
    queryKey: ["lists"],
    queryFn: getListsAction,
  });
}

export function useList(listId: number | null) {
  return useQuery({
    queryKey: ["list", listId],
    queryFn: () => getListAction(listId!),
    enabled: !!listId,
  });
}

export function useUpdateListName() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ listId, name }: { listId: number; name: string }) =>
      updateListNameAction(listId, name),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["list"] });
      queryClient.invalidateQueries({ queryKey: ["lists"] });
      toast({
        title: "List renamed successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to rename list",
        description: error.message || "An error occurred while renaming the list.",
        variant: "destructive",
      });
    },
  });
}

export function useDeleteList() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: deleteListAction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["list"] });
      queryClient.invalidateQueries({ queryKey: ["lists"] });
      toast({
        title: "List deleted successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Failed to delete list",
        description: error.message || "An error occurred while deleting the list.",
        variant: "destructive",
      });
    },
  });
}
