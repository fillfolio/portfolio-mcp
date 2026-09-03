const REQUEST_BYTES = 1_000_000;
const RESPONSE_BYTES = 2_000_000;
const MAX_DEPTH = 12;
const MAX_ARRAY_ITEMS = 200;
const MAX_OBJECT_KEYS = 100;
const MAX_NODES = 5_000;

export type McpBodyValidation =
  | { ok: true; body: Record<string, unknown> }
  | { ok: false; message: string; status: number };

async function readBoundedBody(request: Request, maximum: number) {
  const reader = request.clone().body?.getReader();
  if (!reader) return null;
  const chunks: Uint8Array[] = [];
  let bytes = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    bytes += value.byteLength;
    if (bytes > maximum) {
      await reader.cancel();
      return null;
    }
    chunks.push(value);
  }
  const joined = new Uint8Array(bytes);
  let offset = 0;
  for (const chunk of chunks) {
    joined.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return new TextDecoder().decode(joined);
}

function hasBoundedShape(root: Record<string, unknown>) {
  const stack: Array<{ value: unknown; depth: number }> = [{ value: root, depth: 0 }];
  let nodes = 0;
  while (stack.length) {
    const current = stack.pop()!;
    nodes += 1;
    if (nodes > MAX_NODES || current.depth > MAX_DEPTH) return false;
    if (Array.isArray(current.value)) {
      if (current.value.length > MAX_ARRAY_ITEMS) return false;
      for (const value of current.value) stack.push({ value, depth: current.depth + 1 });
      continue;
    }
    if (current.value && typeof current.value === "object") {
      const values = Object.values(current.value);
      if (values.length > MAX_OBJECT_KEYS) return false;
      for (const value of values) stack.push({ value, depth: current.depth + 1 });
    }
  }
  return true;
}

export async function validateMcpRequestBody(request: Request): Promise<McpBodyValidation> {
  const mediaType = request.headers.get("content-type")?.split(";", 1)[0]?.trim().toLowerCase();
  if (mediaType !== "application/json") return { ok: false, message: "Content-Type must be application/json", status: 415 };

  const rawLength = request.headers.get("content-length");
  if (rawLength && (!/^\d+$/.test(rawLength) || Number(rawLength) > REQUEST_BYTES)) {
    return { ok: false, message: "Request body too large", status: 400 };
  }

  const raw = await readBoundedBody(request, REQUEST_BYTES);
  if (raw === null) return { ok: false, message: "Request body too large", status: 400 };

  let body: unknown;
  try {
    body = JSON.parse(raw);
  } catch {
    return { ok: false, message: "Malformed JSON request", status: 400 };
  }
  if (!body || typeof body !== "object" || Array.isArray(body)) {
    return { ok: false, message: "MCP batch requests are not accepted", status: 400 };
  }
  if (!hasBoundedShape(body as Record<string, unknown>)) {
    return { ok: false, message: "Request structure exceeds MCP limits", status: 400 };
  }
  return { ok: true, body: body as Record<string, unknown> };
}

export async function measureMcpResponse(response: Response) {
  const rawLength = response.headers.get("content-length");
  if (rawLength) {
    if (!/^\d+$/.test(rawLength)) return RESPONSE_BYTES + 1;
    return Number(rawLength);
  }
  const reader = response.clone().body?.getReader();
  if (!reader) return 0;
  let bytes = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) return bytes;
    bytes += value.byteLength;
    if (bytes > RESPONSE_BYTES) {
      await reader.cancel();
      return bytes;
    }
  }
}

export const MCP_RESPONSE_BYTE_LIMIT = RESPONSE_BYTES;
