"use client";

import { useRouter } from "next/navigation";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { useDeleteList } from "../hooks/use-lists";
import { toast } from "@/components/ui/use-toast";
import { Trash2 } from "lucide-react";
import { useState } from "react";

interface DeleteListDialogProps {
  listId: number;
  listName: string;
  isOwner: boolean;
}

export function DeleteListDialog({ listId, listName, isOwner }: DeleteListDialogProps) {
  const router = useRouter();
  const deleteList = useDeleteList();
  const [open, setOpen] = useState(false);

  if (!isOwner) {
    return null;
  }

  const handleDelete = async () => {
    try {
      await deleteList.mutateAsync(listId);
      toast({
        title: "List deleted successfully",
      });
      setOpen(false);
      router.push("/dashboard");
    } catch (err) {
      console.error("Delete error:", err);
      toast({
        title: "Failed to delete list",
        description: err instanceof Error ? err.message : "An error occurred",
        variant: "destructive",
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button type="button" variant="destructive" size="sm">
          <Trash2 className="h-4 w-4 mr-1" />
          Delete List
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete List</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete "{listName}"? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button 
            type="button"
            variant="destructive" 
            onClick={handleDelete}
            disabled={deleteList.isPending}
          >
            {deleteList.isPending ? "Deleting..." : "Delete"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
