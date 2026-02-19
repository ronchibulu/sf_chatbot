import { redirect } from "next/navigation";
import { getSession } from "../lib/auth";
import { headers } from "next/headers";

export default async function HomePage() {
  const session = await getSession({
    headers: await headers(),
  });

  if (session) {
    redirect("/dashboard");
  } else {
    redirect("/register");
  }

  return <div>hihi</div>;
}
