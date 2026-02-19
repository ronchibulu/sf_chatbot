import { NextRequest, NextResponse } from "next/server";
import { getSession } from "@/lib/auth";
import { headers } from "next/headers";

const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ list_id: string }> }
) {
  const { list_id } = await params;
  
  // Validate session
  const session = await getSession({
    headers: await headers(),
  });

  if (!session?.user) {
    return NextResponse.json(
      { detail: "Not authenticated" },
      { status: 401 }
    );
  }

  // Proxy request to FastAPI
  try {
    const response = await fetch(`${FASTAPI_URL}/api/v1/lists/${list_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": session.user.id,
        "X-User-Email": session.user.email || "",
      },
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("FastAPI proxy error:", error);
    return NextResponse.json(
      { detail: "Internal server error" },
      { status: 500 }
    );
  }
}
