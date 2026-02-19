"use client";

import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { Clock } from "lucide-react";

interface DueDateDisplayProps {
  dueDate: Date;
  isCompleted: boolean;
}

export function DueDateDisplay({ dueDate, isCompleted }: DueDateDisplayProps) {
  const now = new Date();
  // Set time to midnight for fair comparison
  now.setHours(0, 0, 0, 0);
  dueDate.setHours(0, 0, 0, 0);

  const isOverdue = !isCompleted && dueDate < now;

  return (
    <Badge
      className={cn(
        "flex items-center p-3 [&>svg]:size-4!",
        isOverdue ? "bg-destructive" : "bg-green-800",
      )}
    >
      <Clock className="size-4 text-white" />
      <span className="text-xs text-white">
        Due Date - {format(dueDate, "MMM d, yyyy")}
      </span>
    </Badge>
  );
}
