Feature: Preserve policy decision evidence
  As an AI governance lead
  I want a Praxis policy decision correlated with tamper-evident evidence
  So that I can reconstruct enforcement without turning a receipt into authorization

  @track3 @preview
  Scenario: Correlate one PPE decision with its ledger receipt
    Given a Praxis request with an exact trace identifier
    And PPE has completed an allow or deny decision
    When the versioned decision is mapped to OCSF and submitted to the immutable ledger
    Then the ledger correlation identifier equals the exact Praxis trace identifier
    And the receipt verifies with its entry hash and entry type
    And the evidence contains no prompt, completion, or credential
    And the receipt is not used as the authorization decision

  @track3 @preview
  Scenario: Report unavailable upstream integration honestly
    Given the pinned Praxis build has no stable PPE audit interface
    When the learner opens the evidence preservation module
    Then the module is identified as a contract-ready preview
    And no live-integration or compliance claim is made

