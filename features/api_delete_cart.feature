Feature: DummyJSON Shopping Cart Lifecycle Deletion

  Scenario Outline: Authenticate profile, create a cart, and execute a secure tear down deletion
    Given the DummyJSON API environment is active
    When the user logs in with username "<username>" and password "<password>" via API
    And creates a dynamic cart session with product IDs "<product_ids>" and quantities "<quantities>"
    And executes a HTTP DELETE operation against an authorized test seed cart ID
    Then the system must confirm deletion with status code 200
    And the returned payload state must show the record is deleted

    Examples:


      | username | password   | product_ids | quantities |
      | emilys   | emilyspass | 1,2         | 1,3        |
