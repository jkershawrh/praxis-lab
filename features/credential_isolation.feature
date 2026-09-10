Feature: Isolate upstream credentials from applications
  Centralized credential handling reduces secret sprawl across application teams.

  Scenario: An application invokes an approved model
    Given the application knows only the Praxis route
    And the provider credential exists only in an OpenShift Secret
    When the application submits a model request
    Then Praxis routes the request to the approved backend
    And the application receives a successful response
    And application configuration and logs do not expose the credential

