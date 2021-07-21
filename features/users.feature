@fixture.browser.gs
Feature: User with different profile view different login options

  @smoke_test @login
  Scenario: I am an admin user, I can view the options
    Given user_admin I am an admin user I can enter the username and password
    Then I can see the home page
