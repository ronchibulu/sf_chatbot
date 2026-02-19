/** Tests for TODO items delete/restore - Story 3.4 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode } from 'react';

// Mock the delete/restore API
vi.mock('../api/delete-todo-item', () => ({
  deleteTodoItemAction: vi.fn(),
  restoreTodoItemAction: vi.fn(),
}));

import { deleteTodoItemAction, restoreTodoItemAction } from '../api/delete-todo-item';
import { useDeleteTodoItem, useRestoreTodoItem } from '../hooks/use-todo-items';

const mockDeleteItem = deleteTodoItemAction as ReturnType<typeof vi.fn>;
const mockRestoreItem = restoreTodoItemAction as ReturnType<typeof vi.fn>;

describe('useDeleteTodoItem', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });
    vi.clearAllMocks();
  });

  const wrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  it('should delete item successfully', async () => {
    mockDeleteItem.mockResolvedValueOnce(undefined);

    const { result } = renderHook(() => useDeleteTodoItem(), { wrapper });

    result.current.mutate({ itemId: 1 });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(mockDeleteItem).toHaveBeenCalledWith(1);
  });

  it('should handle delete error', async () => {
    mockDeleteItem.mockRejectedValueOnce(new Error('Item not found'));

    const { result } = renderHook(() => useDeleteTodoItem(), { wrapper });

    result.current.mutate({ itemId: 999 });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error?.message).toBe('Item not found');
  });
});

describe('useRestoreTodoItem', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });
    vi.clearAllMocks();
  });

  const wrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  it('should restore item successfully', async () => {
    const mockRestoredItem = {
      id: 1,
      listId: 1,
      text: 'Test task',
      status: "not_started" as const,
      createdAt: '2026-01-01T00:00:00',
      updatedAt: '2026-01-02T00:00:00',
      createdBy: 'user-123',
    };

    mockRestoreItem.mockResolvedValueOnce(mockRestoredItem);

    const { result } = renderHook(() => useRestoreTodoItem(), { wrapper });

    result.current.mutate({ itemId: 1 });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(mockRestoreItem).toHaveBeenCalledWith(1);
  });

  it('should handle restore error - timeout', async () => {
    mockRestoreItem.mockRejectedValueOnce(new Error('Undo timeout expired - item cannot be restored'));

    const { result } = renderHook(() => useRestoreTodoItem(), { wrapper });

    result.current.mutate({ itemId: 1 });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });

    expect(result.current.error?.message).toBe('Undo timeout expired - item cannot be restored');
  });
});

describe('Delete/Restore API Actions', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn();
  });

  it('should call DELETE endpoint with correct item ID', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      status: 204,
    });

    const { deleteTodoItemAction } = await import('../api/delete-todo-item');
    await deleteTodoItemAction(1);

    expect(global.fetch).toHaveBeenCalledWith(
      '/api/v1/items/1',
      expect.objectContaining({
        method: 'DELETE',
      })
    );
  });

  it('should call RESTORE endpoint with correct item ID', async () => {
    const mockResponse = {
      ok: true,
      json: vi.fn().mockResolvedValue({
        id: 1,
        list_id: 1,
        text: 'Test task',
        status: 'not_started',
        created_at: '2026-01-01T00:00:00',
        updated_at: '2026-01-02T00:00:00',
        created_by: 'user-123',
      }),
    };

    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce(mockResponse);

    const { restoreTodoItemAction } = await import('../api/delete-todo-item');
    await restoreTodoItemAction(1);

    expect(global.fetch).toHaveBeenCalledWith(
      '/api/v1/items/1/restore',
      expect.objectContaining({
        method: 'POST',
      })
    );
  });

  it('should throw error for 403 forbidden on delete', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 403,
    });

    const { deleteTodoItemAction } = await import('../api/delete-todo-item');

    await expect(deleteTodoItemAction(1)).rejects.toThrow("You don't have permission to delete this item.");
  });

  it('should throw error for 410 Gone on restore (timeout)', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      status: 410,
    });

    const { restoreTodoItemAction } = await import('../api/delete-todo-item');

    await expect(restoreTodoItemAction(1)).rejects.toThrow('Undo timeout expired - item cannot be restored');
  });
});
