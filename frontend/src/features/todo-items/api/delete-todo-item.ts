/** API actions for deleting TODO items. */
import type { TodoItem } from "../types";

export async function deleteTodoItemAction(itemId: number): Promise<void> {
  const response = await fetch(`/api/v1/items/${itemId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Not authenticated. Please log in.");
    }
    if (response.status === 403) {
      throw new Error("You don't have permission to delete this item.");
    }
    if (response.status === 404) {
      throw new Error("Item not found");
    }
    const error = await response
      .json()
      .catch(() => ({ detail: "Failed to delete item" }));
    throw new Error(error.detail || "Failed to delete item");
  }

  // No content returned on successful delete
  return;
}

export async function restoreTodoItemAction(itemId: number): Promise<TodoItem> {
  const response = await fetch(`/api/v1/items/${itemId}/restore`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Not authenticated. Please log in.");
    }
    if (response.status === 403) {
      throw new Error("You don't have permission to restore this item.");
    }
    if (response.status === 404) {
      throw new Error("Item not found or cannot be restored");
    }
    if (response.status === 410) {
      throw new Error("Undo timeout expired - item cannot be restored");
    }
    const error = await response
      .json()
      .catch(() => ({ detail: "Failed to restore item" }));
    throw new Error(error.detail || "Failed to restore item");
  }

  const result = await response.json();
  return result as TodoItem;
}
