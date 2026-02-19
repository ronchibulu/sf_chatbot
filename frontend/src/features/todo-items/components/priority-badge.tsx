"use client";

import { Badge } from "@/components/ui/badge";
import type { Priority } from "../types";

interface PriorityBadgeProps {
  priority: Priority;
}

const priorityStyles: Record<NonNullable<Priority>, string> = {
  low: "bg-gray-500 text-white",
  medium: "bg-[#D9730D] text-white",
  high: "bg-[#E03E3E] text-white",
};

const priorityLabels: Record<NonNullable<Priority>, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
};

export function PriorityBadge({ priority }: PriorityBadgeProps) {
  if (!priority) return null;

  return (
    <Badge className={`flex items-center p-3 ${priorityStyles[priority]}`}>
      {priorityLabels[priority]}
    </Badge>
  );
}
