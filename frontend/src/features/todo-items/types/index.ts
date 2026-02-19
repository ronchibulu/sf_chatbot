/** TypeScript types for TODO items feature. */

export type Priority = "low" | "medium" | "high" | null;

export const todoItemStatusValues = [
  "not_started",
  "in_progress",
  "completed",
] as const;
export type TodoItemStatus = (typeof todoItemStatusValues)[number];

export const todoItemStatusLabel = {
  not_started: "Not Started",
  in_progress: "In Progress",
  completed: "Completed",
};

export interface TodoItem {
  id: number;
  list_id: number;
  text: string;
  description?: string;
  tags?: string[];
  status: TodoItemStatus;
  due_date?: string | null;
  priority?: Priority;
  created_at: string;
  updated_at: string;
  created_by: string;
}

export type UpdateTodoItem = Omit<
  TodoItem,
  "created_at" | "updated_at" | "created_by"
>;

export interface CreateItemData {
  text: string;
  description?: string;
  tags?: string[];
  status?: TodoItemStatus;
}
