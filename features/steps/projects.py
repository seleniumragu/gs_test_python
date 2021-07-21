from behave import then, when

from page_model.create_projects import ProjectsPage, CreateSimulation
from page_model.home_page import TabBar


@when('I can navigate to the projects page')
def step_impl(context):
    context.execute_steps("""given user_admin I am an admin user I can enter the username and password""")
    context.tabs_page = TabBar(context)
    context.tabs_page.click_projects_btn()


@then('I can create a new project')
def step_impl(context):
    for row in context.table:
        context.projects_page = ProjectsPage(context)
        context.projects_page.click_new_project_btn()
        context.projects_page.check_new_project_txt()
        context.projects_page.enter_project_name()
        context.projects_page.enter_project_description(row['project_des'])
        context.projects_page.click_add_btn()


@then('I can create a new simulation')
def step_impl(context):
    # context.execute_steps("""when I can navigate to the projects page""")
    for row in context.table:
        context.simulation_page = CreateSimulation(context)
        context.simulation_page.click_project_expand_icon()
        context.simulation_page.click_new_simulation_btn()
        context.simulation_page.enter_simulation_name()
        context.simulation_page.enter_simulation_description(row['simulation_des'])
        context.simulation_page.click_next_btn()
        context.tabs_page = TabBar(context)
        context.tabs_page.click_projects_btn()
        context.simulation_page.simulation_exists()


