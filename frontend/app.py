# frontend/app.py
from reactpy import component, html, hooks
from frontend.components.sidebar import Sidebar
from frontend.components.pages.home import HomePage
from frontend.components.pages.chat import ChatPage
from frontend.components.pages.profile import ProfilePage
from frontend.styles.common import FONT_FAMILY, LIGHT_BG


@component
def frontend_app():
    authenticated, set_authenticated = hooks.use_state(True)  # Set to True for testing
    current_page, set_page = hooks.use_state("Home")

    # Mock user data for testing
    mock_user = {
        "email": "test@example.com",
        "name": "Test User"
    }

    if not authenticated:
        from components.auth import AuthBox
        return AuthBox(
            on_authenticated=set_authenticated, 
            set_token=lambda x: None,  # Mock function for now
            set_user=lambda x: None    # Mock function for now
        )

    if current_page == "Logout":
        set_authenticated(False)
        set_page("Home")
        return html.div("Logging out...")

    # FIX: Call the component functions directly, don't use lambda
    page_component = {
        "Home": HomePage(),
        "Chat": ChatPage(token="mock-token", user=mock_user),
        "Profile": ProfilePage(user=mock_user),
    }.get(current_page, HomePage())

    return html.div(
        {"style": {
            "display": "flex",
            "minHeight": "100vh",
            "fontFamily": FONT_FAMILY,
            "background": LIGHT_BG
        }},
        Sidebar(current_page, set_page, mock_user),
        html.div({"style": {"flex": 1, "background": LIGHT_BG, "marginLeft": "280px"}}, page_component),
    )