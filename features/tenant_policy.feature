Feature: Enforce tenant model policy
  Platform owners need to limit each tenant to approved model capabilities.

  Scenario: An approved tenant invokes an allowed model
    Given the tenant identity is authenticated
    And the requested model is allowed for that tenant
    When the tenant submits a request through Praxis
    Then the request reaches the allowed backend
    And an attributable policy decision is recorded

  Scenario: A tenant invokes a disallowed model
    Given the tenant identity is authenticated
    And the requested model is not allowed for that tenant
    When the tenant submits a request through Praxis
    Then the request is rejected before reaching the backend
    And the denial is recorded without sensitive request content

