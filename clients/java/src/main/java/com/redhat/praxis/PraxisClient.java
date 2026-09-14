package com.redhat.praxis;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public final class PraxisClient {
    private final HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .build();
    private final URI endpoint;

    public PraxisClient() {
        String baseUrl = requireEnvironment("PRAXIS_BASE_URL").replaceAll("/$", "");
        this.endpoint = URI.create(baseUrl + "/v1/chat/completions");
    }

    public String invoke(String prompt) throws Exception {
        String model = System.getenv().getOrDefault("PRAXIS_MODEL", "lab-model");
        String body = "{\"model\":\"" + escape(model) + "\",\"messages\":[{\"role\":\"user\",\"content\":\""
                + escape(prompt) + "\"}]}";
        HttpRequest request = HttpRequest.newBuilder(endpoint)
                .timeout(Duration.ofSeconds(30))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();
        return client.send(request, HttpResponse.BodyHandlers.ofString()).body();
    }

    public static void main(String[] args) throws Exception {
        String prompt = args.length == 0
                ? "Explain the role of an AI gateway in one sentence."
                : String.join(" ", args);
        System.out.println(new PraxisClient().invoke(prompt));
    }

    private static String requireEnvironment(String name) {
        String value = System.getenv(name);
        if (value == null || value.isBlank()) throw new IllegalStateException(name + " is required");
        return value;
    }

    private static String escape(String value) {
        return value.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
