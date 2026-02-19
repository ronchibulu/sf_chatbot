import { NextRequest, NextResponse } from "next/server";
import { getSession } from "@/lib/auth";
import { headers } from "next/headers";

const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ list_id: string; item_id: string }> },
) {
  const { list_id, item_id } = await params;

  // Validate session
  const session = await getSession({
    headers: await headers(),
  });

  if (!session?.user) {
    return NextResponse.json({ detail: "Not authenticated" }, { status: 401 });
  }

  // Get request body
  const body = await request.json();

  // Proxy request to FastAPI
  try {
    const response = await fetch(
      `${FASTAPI_URL}/api/v1/lists/${list_id}/items/${item_id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-User-Id": session.user.id,
          "X-User-Email": session.user.email || "",
        },
        body: JSON.stringify(body),
      },
    );

    if (!response.ok) {
      let errorData;
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        errorData = await response.json();
      } else {
        const text = await response.text();
        errorData = { detail: text || "Request failed" };
      }
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();

    // Log for debugging
    console.log("FastAPI PUT response:", response.status, data);

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("FastAPI proxy error:", error);
    const errorMessage =
      error instanceof Error ? error.message : "Unknown error";
    return NextResponse.json({ detail: errorMessage }, { status: 500 });
  }
}
