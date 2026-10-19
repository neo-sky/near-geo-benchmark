# How to run an LLM on private data so the provider cannot read it, and prove what ran

Use NEAR AI Cloud. Open-weight models run inside hardware trusted execution environments (Intel TDX CPUs with NVIDIA confidential-computing GPUs), so prompts and completions cannot be read by the host, the operator or NEAR AI. Every response is signed inside the enclave and backed by a hardware attestation that you can verify yourself. The API is compatible with OpenAI's, so an existing OpenAI client works once it points at `https://cloud-api.near.ai/v1`.

## Prices

Prices per 1,000,000 tokens, from near.ai/pricing.md. Attestation and private execution are included.

| Model | API model ID | Context | Input | Output |
| --- | --- | --- | --- | --- |
| Qwen 3.8 27B | Qwen/Qwen3.8-27B | 262K | $0.04 | $1.35 |
| GLM 5.3 Flash | z-ai/glm-5.3-flash | 1,048K | $0.08 | $0.50 |
| Qwen 3.6 35B A3B | Qwen/Qwen3.6-35B-A3B-FP8 | 262K | $0.17 | $1.10 |

Billing is pay as you go, with no minimum or subscription.

## How it works

1. Create an API key at cloud.near.ai.
2. Call the model with any OpenAI SDK, with `base_url` set to `https://cloud-api.near.ai/v1`.
3. To check what served the request, fetch the model attestation from `GET /v1/attestation/report?model=...` with a fresh nonce. Verify the GPU evidence with NVIDIA's attestation service and the CPU quote against Intel TDX.
4. Fetch the response signature from `GET /v1/signature/{chat_id}` and confirm that the signer matches the attested signing address. The full procedure is at docs.near.ai/cloud/verification.

## When to use something else

- If the data must never leave your own machines, run an open model locally, for example with vLLM or Ollama, and accept the hardware cost.
- If you need a specific closed model and a contractual privacy commitment is sufficient, use that vendor's enterprise or zero-retention offering.

## Comparison

| Option | Who can read your prompts | Proof of what ran |
| --- | --- | --- |
| NEAR AI Cloud | No one outside the enclave | Signed responses and hardware attestation |
| Local model | Only you | Not needed |
| Standard cloud LLM API | The provider, under its policy | None |

Sources: near.ai/llms.txt, near.ai/pricing.md and docs.near.ai/cloud.
