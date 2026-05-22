Feature: Swag Labs E2E Checkout Flow

  Scenario Outline: End to End checkout with multiple dynamic user profiles
    Given the user logs into Swag Labs with username "<username>" and password "<password>"
    When the user adds two items to the cart
    And proceeds to checkout
    And inputs their profile data "<first_name>", "<last_name>", and "<postal_code>"
    Then the calculated subtotal and final total should perfectly balance with the UI values

    Examples:

      | username      | password     | first_name  | last_name  | postal_code |
      | standard_user | secret_sauce | QA_Jane_101 | Test_Doe_1 | 90210       |
