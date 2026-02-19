import { redirect } from "next/navigation";
import { getSession } from "@/lib/auth";
import { headers } from "next/headers";
import { DashboardClient } from "./dashboard-client";

export default async function DashboardPage() {
  const session = await getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/login?message=Please log in to continue");
  }

  return <DashboardClient session={session} />;
}
