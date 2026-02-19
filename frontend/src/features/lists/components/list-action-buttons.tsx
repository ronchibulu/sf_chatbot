"use client";

import { Button } from "@/components/ui/button";
import { Share2, Pencil } from "lucide-react";
import { DeleteListDialog } from "./delete-list-dialog";

interface ListActionButtonsProps {
  listId: number;
  listName: string;
  isOwner: boolean;
  onEditClick?: () => void;
}

export function ListActionButtons({
  listId,
  listName,
  isOwner,
  onEditClick,
}: ListActionButtonsProps) {
  return (
    <div className="flex gap-2">
      {isOwner && (
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={onEditClick}
          title="Edit list name"
        >
          <Pencil className="h-4 w-4 mr-1" />
          Edit Name
        </Button>
      )}
      <DeleteListDialog listId={listId} listName={listName} isOwner={isOwner} />
    </div>
  );
}
