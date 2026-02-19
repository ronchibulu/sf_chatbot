"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2, List } from "lucide-react";
import { useCreateList } from "../hooks/use-lists";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

const createListSchema = z.object({
  name: z
    .string()
    .min(1, "List name is required")
    .max(255, "List name must be 255 characters or less"),
});

type CreateListFormData = z.infer<typeof createListSchema>;

interface CreateListModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CreateListModal({ open, onOpenChange }: CreateListModalProps) {
  const createList = useCreateList();

  const form = useForm<CreateListFormData>({
    resolver: zodResolver(createListSchema),
    mode: "onBlur",
    defaultValues: {
      name: "",
    },
  });

  const onSubmit = async (data: CreateListFormData) => {
    await createList.mutateAsync({ name: data.name });
    form.reset();
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <List className="size-5" />
            Create New List
          </DialogTitle>
          <DialogDescription>
            Create a new TODO list to organize your tasks.
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>List Name</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="e.g., Work Tasks, Shopping List"
                      autoFocus
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => onOpenChange(false)}
                disabled={createList.isPending}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={createList.isPending}
              >
                {createList.isPending ? (
                  <>
                    <Loader2 className="animate-spin" />
                    Creating...
                  </>
                ) : (
                  "Create List"
                )}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
