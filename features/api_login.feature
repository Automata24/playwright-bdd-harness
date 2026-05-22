Feature: DummyJSON Authentication API Verification

  Scenario Outline: Verify successful user authentication via authentication endpoint
    Given the DummyJSON authentication endpoint is initialized
    When a POST request is dispatched with user "<username>" and password "<password>"
    Then the response status code must be 200
    And the response payload must return a valid token string

    Examples:


      | username   | password    |
      | emilys     | emilyspass  |
