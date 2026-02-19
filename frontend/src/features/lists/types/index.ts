/** TypeScript types for TODO lists feature. */

export interface TodoList {
  id: number;
  name: string;
  ownerId: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateListData {
  name: string;
}
