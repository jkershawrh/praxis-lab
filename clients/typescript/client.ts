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

const isMain = process.argv[1]?.endsWith("client.ts");
if (isMain) {
  const prompt = process.argv.slice(2).join(" ") || "Explain the role of an AI gateway in one sentence.";
  invoke(prompt)
    .then((result) => console.log(JSON.stringify(result, null, 2)))
    .catch((error: unknown) => {
      console.error(error instanceof Error ? error.message : String(error));
      process.exitCode = 1;
    });
}
