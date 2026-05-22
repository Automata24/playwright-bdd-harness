Feature: DummyJSON Defensive API Failure Verification

  # Endpoint 1: /auth/login
  Scenario Outline: Verify authentication microservice safely rejects invalid parameter payload schemas
    Given the dynamic DummyJSON REST context is ready
    When an unauthorized POST login request is dispatched with username "<username>" and password "<password>"
    Then the API endpoint must reject the operation with status code 400
    And the failure payload must explicitly state the system error message "<expected_error>"

    Examples:

      | username     | password       | expected_error                 |
      | compromised  | invalid_phrase | Invalid credentials            |

  # Endpoint 2: /products/{id}
  Scenario Outline: Verify product inventory system returns clean resource bounds handling
    Given the dynamic DummyJSON REST context is ready
    When an out of bounds GET request is executed for non existent product ID "<out_of_bounds_id>"
    Then the API endpoint must reject the operation with status code 404
    And the failure payload must explicitly state the system error message "<expected_error>"

    Examples:

      | out_of_bounds_id | expected_error                       |
      | 999999           | Product with id '999999' not found   |
