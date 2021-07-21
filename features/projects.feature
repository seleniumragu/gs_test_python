@fixture.browser.gs
Feature: create projects

  @smoke_test @create_project
  Scenario: I am an admin user, I can create projects
    When I can navigate to the projects page
    Then I can create a new project
    |project_des          |
    |This is a new project|

  @smoke_test @create_simulation
  Scenario: I am an admin user, I can create simulation
    Then I can create a new simulation
    |simulation_des          |
    |This is a new simulation|
