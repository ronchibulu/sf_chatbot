/** API action for deleting a list. */
export async function deleteListAction(listId: number): Promise<void> {
  const response = await fetch(`/api/lists/${listId}`, {
    method: "DELETE",
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
    throw new Error("Failed to delete list");
  }

  return;
}
