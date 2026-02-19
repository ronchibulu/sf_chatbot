/** API actions for TODO items. */
import type { TodoItem, CreateItemData } from "../types";

export async function createTodoItemAction(
  listId: number,
  data: CreateItemData,
): Promise<TodoItem> {
  const response = await fetch(`/api/lists/${listId}/items`, {
    method: "POST",
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
      throw new Error("You don't have access to add items to this list.");
    }
    if (response.status === 400) {
      const error = await response
        .json()
        .catch(() => ({ detail: "Invalid request" }));
      throw new Error(error.detail || "Failed to create item");
    }
    const error = await response
      .json()
      .catch(() => ({ detail: "Failed to create item" }));
    throw new Error(error.detail || "Failed to create item");
  }

  const result = await response.json();
  return result as TodoItem;
}

export async function getTodoItemsAction(listId: number): Promise<TodoItem[]> {
  const response = await fetch(`/api/lists/${listId}/items`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Not authenticated. Please log in.");
    }
    if (response.status === 403) {
      throw new Error("You don't have access to this list.");
    }
    if (response.status === 404) {
      throw new Error("List not found");
    }
    throw new Error("Failed to fetch items");
  }

  const results = await response.json();
  return results as TodoItem[];
}
