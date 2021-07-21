from page_model.home_page import TabBar

from behave import then


@then("I can click the projects icon")
def step_impl(context):
    context.tabs_page = TabBar(context)
    context.tabs_page.click_projects_btn()
