import { redirect } from "next/navigation"
import { getSession } from "@/lib/auth"
import { headers } from "next/headers"
import { AppShell } from "@/components/app-shell"

export default async function AuthenticatedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await getSession({
    headers: await headers(),
  })

  if (!session) {
    redirect("/login?message=Please log in to continue")
  }

  return <AppShell session={session}>{children}</AppShell>
}
