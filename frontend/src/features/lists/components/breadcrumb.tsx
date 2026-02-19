"use client";

import Link from "next/link";

interface BreadcrumbNavProps {
  listName: string;
}

export function BreadcrumbNav({ listName }: BreadcrumbNavProps) {
  return (
    <nav className="flex items-center space-x-2 text-sm">
      <Link 
        href="/dashboard" 
        className="text-primary hover:underline"
      >
        Dashboard
      </Link>
      <span className="text-muted-foreground">/</span>
      <span className="text-foreground">{listName}</span>
    </nav>
  );
}
