const BASE_URL = "https://1click.chaindefuser.com";
const TIMEOUT_MS = 15_000;
const QUOTE_WINDOW_MS = 30 * 60 * 1000;

export type Token = {
  assetId: string;
  symbol: string;
  blockchain: string;
  decimals: number;
  price?: number;
  contractAddress?: string;
};

export type QuoteInput = {
  originAsset: string;
  destinationAsset: string;
  amount: string;
  swapType: "EXACT_INPUT" | "EXACT_OUTPUT";
  recipient: string;
  refundTo: string;
  slippageBps: number;
};

export type Quote = {
  amountIn: string;
  amountInFormatted: string;
  amountInUsd?: string;
  amountOut: string;
  amountOutFormatted: string;
  amountOutUsd?: string;
  minAmountOut?: string;
  minAmountIn?: string;
  timeEstimate?: number;
  deadline?: string;
};

export type TransferStatus = {
  status: string;
  updatedAt?: string;
  swapDetails?: Record<string, unknown>;
};

export class OneClickError extends Error {
  constructor(
    readonly status: number,
    detail: string,
  ) {
    super(`1Click API returned ${status}: ${detail}`);
  }
}

export type OneClickClient = ReturnType<typeof createClient>;

export function createClient(apiKey: string | undefined) {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (apiKey) headers["X-API-Key"] = apiKey;

  const request = async <T>(path: string, init: RequestInit = {}): Promise<T> => {
    const res = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers,
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    const body: unknown = await res.json().catch(() => null);
    if (!res.ok) throw new OneClickError(res.status, errorDetail(body));
    return body as T;
  };

  return {
    tokens: () => request<Token[]>("/v0/tokens"),
    quote: (input: QuoteInput) =>
      request<{ quote: Quote }>("/v0/quote", {
        method: "POST",
        body: JSON.stringify(previewRequest(input)),
      }).then((res) => res.quote),
    status: (depositAddress: string, depositMemo?: string) => {
      const query = new URLSearchParams({ depositAddress });
      if (depositMemo) query.set("depositMemo", depositMemo);
      return request<TransferStatus>(`/v0/status?${query}`);
    },
  };
}

function previewRequest(input: QuoteInput) {
  return {
    dry: true,
    swapType: input.swapType,
    slippageTolerance: input.slippageBps,
    originAsset: input.originAsset,
    depositType: "ORIGIN_CHAIN",
    destinationAsset: input.destinationAsset,
    amount: input.amount,
    refundTo: input.refundTo,
    refundType: "ORIGIN_CHAIN",
    recipient: input.recipient,
    recipientType: "DESTINATION_CHAIN",
    deadline: new Date(Date.now() + QUOTE_WINDOW_MS).toISOString(),
  };
}

function errorDetail(body: unknown) {
  if (body && typeof body === "object" && "message" in body) {
    const message = (body as { message: unknown }).message;
    return Array.isArray(message) ? message.join("; ") : String(message);
  }
  return "no error detail";
}
