Feature: Replace the inference backend without changing clients
  Platform teams need to move between lab and enterprise model endpoints while preserving application contracts.

  Scenario Outline: Invoke an equivalent model through a configured backend
    Given Praxis is configured with the "<backend>" inference endpoint
    And the upstream credential is stored only in an OpenShift Secret
    And each client knows only the Praxis route
    When the Java, Python, and TypeScript clients submit equivalent requests
    Then each request is routed through Praxis
    And each client receives a protocol-valid response
    And no client contains backend-specific configuration

    Examples:
      | backend                    |
      | RHPDS MaaS                 |
      | Red Hat OpenShift AI       |
      | OpenAI-compatible endpoint |

