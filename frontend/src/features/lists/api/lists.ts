/** API actions for TODO lists. */
import type { TodoList, CreateListData } from "../types";

export async function createListAction(
  data: CreateListData,
): Promise<TodoList> {
  const response = await fetch("/api/lists", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: data.name }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Not authenticated. Please log in.");
    }
    const error = await response
      .json()
      .catch(() => ({ detail: "Failed to create list" }));
    throw new Error(error.detail || "Failed to create list");
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

export async function getListsAction(): Promise<TodoList[]> {
  const response = await fetch("/api/lists", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Not authenticated. Please log in.");
    }
    throw new Error("Failed to fetch lists");
  }

  const results = await response.json();

  // Convert snake_case to camelCase for each list
  return results.map(
    (result: {
      id: number;
      name: string;
      owner_id: string;
      created_at: string;
      updated_at: string;
    }) => ({
      id: result.id,
      name: result.name,
      ownerId: result.owner_id,
      createdAt: result.created_at,
      updatedAt: result.updated_at,
    }),
  );
}

export async function getListAction(listId: number): Promise<TodoList> {
  const response = await fetch(`/api/lists/${listId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  console.log("Response status:", response.status);

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
    throw new Error("Failed to fetch list");
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
