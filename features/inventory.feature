Feature: Swag Labs Catalog Inventory Verification

  Scenario Outline: Verify inventory catalog sorting behavior from Z to A
    Given the user logs into Swag Labs with username "<username>" and password "<password>"
    And the catalog is explicitly set to the default A to Z sorting mode
    When the user filters products by "Name (Z to A)" using selection value "za"
    Then the displayed items must be perfectly organized in alphabetical descending order

    Examples:


      | username      | password     |
      | standard_user | secret_sauce |
