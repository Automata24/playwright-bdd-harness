Feature: DummyJSON End-to-End API Integration

  Scenario Outline: Authenticate profile and dynamically generate a three item cart
    Given the DummyJSON API environment is available
    When the user logs in with username "<username>" and password "<password>" via API
    And dispatches a POST request to generate a cart using dynamic profile ID with product IDs "<product_ids>" and quantities "<quantities>"
    Then the system must confirm creation with status code 201
    And the api response total fields must perfectly balance with the product objects

    Examples:


      | username | password   | product_ids | quantities |
      | emilys   | emilyspass | 1,2,15      | 1,3,2      |
