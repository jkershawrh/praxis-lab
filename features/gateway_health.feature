Feature: Report gateway health accurately
  OpenShift must distinguish a ready gateway from one that cannot serve traffic.

  Scenario: Praxis is ready to accept requests
    Given the Praxis deployment has valid configuration
    And its required dependencies are available
    When OpenShift evaluates the readiness probe
    Then the readiness probe succeeds

  Scenario: Praxis cannot start with invalid configuration
    Given the Praxis deployment has invalid configuration
    When OpenShift starts the workload
    Then the workload does not become ready
    And the failure is diagnosable without exposing secrets

