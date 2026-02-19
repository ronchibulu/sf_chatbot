"use client";

import { useState } from "react";
import { format, parseISO } from "date-fns";
import { MoreHorizontal, Calendar as CalendarIcon } from "lucide-react";
import { useUpdateTodoItem } from "../hooks/use-todo-items";
import type { Priority, TodoItem } from "../types";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";

interface MoreOptionsDropdownProps {
  item: TodoItem;
  currentDueDate?: string | null;
  currentPriority?: Priority;
}

export function MoreOptionsDropdown({
  item,
  currentDueDate,
  currentPriority,
}: MoreOptionsDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isCalendarOpen, setIsCalendarOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(
    currentDueDate ? new Date(currentDueDate) : undefined,
  );

  const updateItem = useUpdateTodoItem();

  const handleSetDueDate = async () => {
    if (!selectedDate) return;

    try {
      await updateItem.mutateAsync({
        ...item,
        due_date: format(selectedDate, "yyyy-MM-dd"),
      });
      setIsOpen(false);
    } catch (error) {
      // Error handling is done in the hook
    }
  };

  const handleClearDueDate = async () => {
    try {
      await updateItem.mutateAsync({
        ...item,
        due_date: null,
      });
      setSelectedDate(undefined);
      setIsOpen(false);
    } catch (error) {
      // Error handling is done in the hook
    }
  };

  const handleSetPriority = async (priority: string) => {
    try {
      await updateItem.mutateAsync({
        ...item,
        priority: priority as Priority,
      });
      setIsOpen(false);
    } catch (error) {
      // Error handling is done in the hook
    }
  };

  const handleClearPriority = async () => {
    try {
      await updateItem.mutateAsync({
        ...item,
        priority: null,
      });
      setIsOpen(false);
    } catch (error) {
      // Error handling is done in the hook
    }
  };

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8 text-muted-foreground hover:text-primary"
        >
          <MoreHorizontal className="h-4 w-4 text-muted-foreground" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-64 p-2" align="end">
        <div className="flex flex-col gap-3">
          {/* Due Date Section */}
          <div className="space-y-2">
            <div className="text-sm font-medium flex items-center gap-2">
              <CalendarIcon className="h-4 w-4" />
              Set due date
            </div>
            <Popover open={isCalendarOpen} onOpenChange={setIsCalendarOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant={"outline"}
                  className="w-full justify-start"
                  disabled={updateItem.isPending}
                >
                  {selectedDate
                    ? format(selectedDate, "MMM d, yyyy")
                    : "Pick a date"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={selectedDate}
                  onSelect={(date) => {
                    setSelectedDate(date);
                    setIsCalendarOpen(false);
                  }}
                  disabled={(date) =>
                    date < new Date(new Date().setHours(0, 0, 0, 0))
                  }
                  className="rounded-lg"
                  captionLayout="dropdown"
                />
              </PopoverContent>
            </Popover>
            <div className="flex gap-2">
              <Button
                size="sm"
                onClick={handleSetDueDate}
                disabled={!selectedDate || updateItem.isPending}
              >
                {updateItem.isPending ? "Saving..." : "Save"}
              </Button>
              {currentDueDate && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleClearDueDate}
                  disabled={updateItem.isPending}
                >
                  Clear
                </Button>
              )}
            </div>
          </div>

          {/* Priority Section */}
          <div className="space-y-2">
            <div className="text-sm font-medium flex items-center gap-2">
              <span className="w-4 h-4 rounded bg-gray-500 inline-block" />
              Set priority
            </div>
            <div className="flex flex-col gap-1">
              {(["low", "medium", "high"] as const).map((priority) => (
                <Button
                  key={priority}
                  variant="ghost"
                  className="justify-start gap-2"
                  onClick={() => handleSetPriority(priority)}
                  disabled={updateItem.isPending}
                >
                  <span
                    className={`w-3 h-3 rounded ${
                      priority === "low"
                        ? "bg-gray-500"
                        : priority === "medium"
                          ? "bg-[#D9730D]"
                          : "bg-[#E03E3E]"
                    }`}
                  />
                  {priority.charAt(0).toUpperCase() + priority.slice(1)}
                </Button>
              ))}
              {currentPriority && (
                <Button
                  variant="ghost"
                  className="justify-start text-muted-foreground"
                  onClick={handleClearPriority}
                  disabled={updateItem.isPending}
                >
                  Clear
                </Button>
              )}
            </div>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
