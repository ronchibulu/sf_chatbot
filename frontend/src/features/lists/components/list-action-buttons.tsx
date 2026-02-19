"use client";

import { Button } from "@/components/ui/button";
import { Share2, Pencil, Trash2 } from "lucide-react";

interface ListActionButtonsProps {
  listId: number;
  listName: string;
  onEditClick?: () => void;
}

export function ListActionButtons({ listId, listName, onEditClick }: ListActionButtonsProps) {
  return (
    <div className="flex gap-2">
      <Button variant="outline" size="sm" disabled title="Coming in Epic 4">
        <Share2 className="h-4 w-4 mr-1" />
        Share
      </Button>
      <Button variant="outline" size="sm" onClick={onEditClick} title="Edit list name">
        <Pencil className="h-4 w-4 mr-1" />
        Edit Name
      </Button>
      <Button variant="destructive" size="sm" disabled title="Coming in Story 2.5">
        <Trash2 className="h-4 w-4 mr-1" />
        Delete List
      </Button>
    </div>
  );
}
