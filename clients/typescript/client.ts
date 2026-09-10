type ChatResponse = {
  model: string;
  choices: Array<{ message: { role: string; content: string } }>;
};

export async function invoke(prompt: string): Promise<ChatResponse> {
  const baseUrl = process.env.PRAXIS_BASE_URL;
  if (!baseUrl) throw new Error("PRAXIS_BASE_URL is required");

  const response = await fetch(`${baseUrl.replace(/\/$/, "")}/v1/chat/completions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: process.env.PRAXIS_MODEL ?? "lab-model",
      messages: [{ role: "user", content: prompt }],
    }),
  });
  if (!response.ok) throw new Error(`Praxis returned HTTP ${response.status}`);
  return (await response.json()) as ChatResponse;
}

