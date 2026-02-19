"use client";

/** API actions for updating TODO items. */
import type { TodoItem, TodoItemStatus, UpdateTodoItem } from "../types";

export async function updateTodoItemAction(
  data: UpdateTodoItem,
): Promise<TodoItem> {
  // Filter out undefined values to allow partial updates
  // Only include fields that are explicitly provided

  console.log("Updating item with data:", data);

  const response = await fetch(`/api/lists/${data.list_id}/items/${data.id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Not authenticated. Please log in.");
    }
    if (response.status === 403) {
      throw new Error("You don't have permission to edit this item.");
    }
    if (response.status === 404) {
      throw new Error("Item not found");
    }
    if (response.status === 400) {
      const error = await response
        .json()
        .catch(() => ({ detail: "Invalid request" }));
      throw new Error(error.detail || "Failed to update item");
    }
    if (response.status === 422) {
      const error = await response
        .json()
        .catch(() => ({ detail: "Validation error" }));
      console.error("Validation error:", error);
      throw new Error(error.detail || "Validation error");
    }
    const error = await response
      .json()
      .catch(() => ({ detail: "Failed to update item" }));
    throw new Error(error.detail || "Failed to update item");
  }

  const result = await response.json();
  return result as TodoItem;
}
