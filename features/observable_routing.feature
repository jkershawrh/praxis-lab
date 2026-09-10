Feature: Visualize exact request routing evidence
  Learners need to see what the gateway did without inferring behavior from terminal output.

  Scenario: A routed request has matching UI and trace evidence
    Given the Track 2 UI creates a unique W3C trace context
    And Praxis tracing is configured
    When the learner submits a model request
    Then the UI shows the client to Praxis to backend path
    And the selected logical model and request outcome are visible
    And the trace link resolves the exact trace ID created for that request
    And no credential or authorization header is displayed

  Scenario: Trace evidence has not arrived
    Given a request has completed
    And its exact trace ID is not yet queryable
    When the UI checks for trace evidence
    Then the UI reports that trace evidence is pending or unavailable
    And the UI does not display the most recent unrelated trace

