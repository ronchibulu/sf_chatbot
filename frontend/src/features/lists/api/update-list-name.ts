/** API action for updating list name. */
import type { TodoList } from "../types";

export async function updateListNameAction(listId: number, name: string): Promise<TodoList> {
  const response = await fetch(`/api/lists/${listId}/name`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Not authenticated. Please log in.");
    }
    if (response.status === 404) {
      throw new Error("List not found");
    }
    if (response.status === 403) {
      throw new Error("You don't have access to this list");
    }
    const error = await response.json().catch(() => ({ detail: "Failed to update list name" }));
    throw new Error(error.detail || "Failed to update list name");
  }

  const result = await response.json();
  
  // Convert snake_case to camelCase
  return {
    id: result.id,
    name: result.name,
    ownerId: result.owner_id,
    createdAt: result.created_at,
    updatedAt: result.updated_at,
  };
}
