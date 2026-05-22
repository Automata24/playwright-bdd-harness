Feature: Swag Labs Authentication Failures

  Scenario Outline: Verify error messaging on invalid login attempts
    Given the user opens the Swag Labs login page
    When the user attempts to log in with invalid username "<username>" and password "<password>"
    Then a security error message saying "<error_message>" must be displayed

    Examples:

      | username       | password       | error_message                                                              |
      | invalid_user   | secret_sauce   | Epic sadface: Username and password do not match any user in this service  |
      | standard_user  | wrong_password | Epic sadface: Username and password do not match any user in this service  |
