Feature: DummyJSON Products API Verification

  Scenario Outline: Fetch individual product profiles and audit payload schema integrity
    Given the DummyJSON API framework is ready
    When a GET request is dispatched to fetch product id "<product_id>"
    Then the system must respond with status code 200
    And the product description string length must exceed 10 characters
    And the primary thumbnail image must utilize an active URL string

    Examples:


      | product_id |
      | 1          |
