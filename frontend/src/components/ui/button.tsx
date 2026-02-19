import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { Slot } from "radix-ui"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-body font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
  {
    variants: {
      variant: {
        // Primary action button (main actions like Create, Save, Invite)
        default: "bg-primary text-primary-foreground hover:bg-primary/90 shadow-xs",
        // Destructive button (delete, remove actions)
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow-xs",
        // Secondary button (cancel, back actions)
        outline: "border border-border bg-background hover:bg-surface shadow-xs",
        // Secondary solid button
        secondary: "bg-secondary text-secondary-foreground hover:bg-surface",
        // Ghost button (inline actions like edit, more)
        ghost: "hover:bg-surface",
        // Link style button
        link: "text-primary underline-offset-4 hover:underline",
        // Success button (for completed states)
        success: "bg-success text-success-foreground hover:bg-success/90 shadow-xs",
      },
      size: {
        default: "h-10 px-4 py-2 has-[>svg]:px-3",
        sm: "h-9 rounded-md gap-1.5 px-3 text-small has-[>svg]:px-2.5",
        lg: "h-11 rounded-lg px-6 has-[>svg]:px-4 text-body",
        icon: "size-10",
        "icon-sm": "size-9",
        "icon-lg": "size-11",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant = "default",
  size = "default",
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot.Root : "button"

  return (
    <Comp
      data-slot="button"
      data-variant={variant}
      data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
