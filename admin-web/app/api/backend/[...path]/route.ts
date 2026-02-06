import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const BACKEND_BASE = process.env.BACKEND_INTERNAL_URL || "http://localhost:8001";

const buildTarget = (path: string) => {
  const clean = path.replace(/^\/+/, "");
  return `${BACKEND_BASE}/${clean}`;
};

const handler = async (request: Request, context: { params: { path: string[] } }) => {
  const url = new URL(request.url);
  const target = new URL(buildTarget(context.params.path.join("/")));
  target.search = url.search;

  const headers = new Headers(request.headers);
  headers.delete("host");

  const body =
    request.method === "GET" || request.method === "HEAD"
      ? undefined
      : await request.arrayBuffer();

  const response = await fetch(target.toString(), {
    method: request.method,
    headers,
    body
  });

  const responseHeaders = new Headers(response.headers);
  return new NextResponse(await response.arrayBuffer(), {
    status: response.status,
    headers: responseHeaders
  });
};

export { handler as GET, handler as POST, handler as PUT, handler as PATCH, handler as DELETE };
