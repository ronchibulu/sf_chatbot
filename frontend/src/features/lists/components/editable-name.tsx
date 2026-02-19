"use client";

import { useState, useRef, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { useUpdateListName } from "../hooks/use-lists";

interface EditableNameProps {
  listId: number;
  name: string;
  isOwner: boolean;
  isEditing?: boolean;
  onEditComplete?: () => void;
}

export function EditableName({ 
  listId, 
  name, 
  isOwner, 
  isEditing: externalIsEditing,
  onEditComplete 
}: EditableNameProps) {
  const [internalIsEditing, setInternalIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(name);
  const [error, setError] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  
  const updateName = useUpdateListName();

  // Use external state if provided, otherwise use internal
  const isEditing = externalIsEditing !== undefined ? externalIsEditing : internalIsEditing;

  // Auto-focus when entering edit mode
  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isEditing]);

  // Reset edit value when name prop changes
  useEffect(() => {
    setEditValue(name);
  }, [name]);

  const handleStartEdit = () => {
    if (!isOwner) return;
    setEditValue(name);
    setInternalIsEditing(true);
    setError("");
  };

  const handleSave = async () => {
    // Validation
    if (!editValue.trim()) {
      setError("List name cannot be empty");
      return;
    }
    if (editValue.length > 255) {
      setError("List name must be 255 characters or less");
      return;
    }

    try {
      await updateName.mutateAsync({ listId, name: editValue.trim() });
      setInternalIsEditing(false);
      onEditComplete?.();
    } catch (err) {
      // Error is handled by useUpdateListName hook
    }
  };

  const handleCancel = () => {
    setEditValue(name);
    setInternalIsEditing(false);
    onEditComplete?.();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSave();
    } else if (e.key === "Escape") {
      handleCancel();
    }
  };

  // Non-owner sees static text
  if (!isOwner) {
    return <h1 className="text-3xl font-bold">{name}</h1>;
  }

  // Edit mode
  if (isEditing) {
    return (
      <div className="flex flex-col gap-1">
        <Input
          ref={inputRef}
          value={editValue}
          onChange={(e) => setEditValue(e.target.value)}
          onKeyDown={handleKeyDown}
          className={error ? "border-red-500" : ""}
        />
        {error && <p className="text-sm text-red-500">{error}</p>}
      </div>
    );
  }

  // Display mode - clickable
  return (
    <h1 
      className="text-3xl font-bold cursor-pointer hover:text-primary transition-colors"
      onClick={handleStartEdit}
    >
      {name}
    </h1>
  );
}
