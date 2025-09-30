# frontend/components/auth.py
from reactpy import component, html, hooks
from frontend.styles.colors import *
from frontend.styles.common import get_input_styles, get_button_styles, FONT_FAMILY
import json


@component
def AuthBox(on_authenticated, set_token, set_user):
    email, set_email = hooks.use_state("")
    password, set_password = hooks.use_state("")
    error_msg, set_error_msg = hooks.use_state("")
    loading, set_loading = hooks.use_state(False)
    is_login, set_is_login = hooks.use_state(True)
    
    # Hover state for buttons
    login_hover, set_login_hover = hooks.use_state(False)
    toggle_hover, set_toggle_hover = hooks.use_state(False)

    async def handle_auth(event):
        if not email or not password:
            set_error_msg("Please fill in all fields")
            return

        set_loading(True)
        set_error_msg("")

        try:
            # For now, use mock authentication
            # You can replace this with actual API calls later
            if email and password:
                # Mock successful login
                set_token("mock-token-12345")
                set_user({"email": email, "name": email.split('@')[0]})
                on_authenticated(True)
            else:
                set_error_msg("Please enter both email and password")

        except Exception as e:
            set_error_msg(f"Error: {str(e)}")
        finally:
            set_loading(False)

    def get_login_button_style():
        base_style = get_button_styles("primary")
        if login_hover and not loading:
            base_style.update({
                "transform": "translateY(-1px)",
                "boxShadow": HOVER_SHADOW
            })
        return base_style

    return html.div(
        {"style": {
            "border": f"1px solid {BORDER_COLOR}",
            "padding": "2.5rem",
            "borderRadius": "12px",
            "maxWidth": "420px",
            "margin": "4rem auto",
            "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.08)",
            "background": WHITE,
            "fontFamily": FONT_FAMILY
        }},
        html.div(
            {"style": {
                "textAlign": "center",
                "marginBottom": "2rem"
            }},
            html.div({
                "style": {
                    "background": PRIMARY_GRADIENT,
                    "width": "60px",
                    "height": "60px",
                    "borderRadius": "12px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "margin": "0 auto 1rem",
                    "color": WHITE,
                    "fontSize": "1.5rem"
                }
            }, "🏥"),
            html.h2({
                "style": {
                    "marginBottom": "0.5rem",
                    "color": TEXT_PRIMARY,
                    "fontWeight": "600",
                    "fontSize": "1.5rem"
                }
            }, "Welcome to Health AI"),
            html.p({
                "style": {
                    "color": TEXT_TERTIARY,
                    "margin": "0",
                    "fontSize": "0.9rem"
                }
            }, "Sign in to your health assistant account")
        ),

        html.div(
            {"style": {"marginBottom": "1.5rem"}},
            html.label({
                "style": {
                    "display": "block",
                    "marginBottom": "0.5rem",
                    "color": TEXT_SECONDARY,
                    "fontWeight": "500",
                    "fontSize": "0.9rem"
                }
            }, "Email"),
            html.input({
                "type": "email",
                "value": email,
                "on_change": lambda e: set_email(e["target"]["value"]),
                "placeholder": "Enter your email",
                "style": get_input_styles(),
            }),
        ),

        html.div(
            {"style": {"marginBottom": "2rem"}},
            html.label({
                "style": {
                    "display": "block",
                    "marginBottom": "0.5rem",
                    "color": TEXT_SECONDARY,
                    "fontWeight": "500",
                    "fontSize": "0.9rem"
                }
            }, "Password"),
            html.input({
                "type": "password",
                "value": password,
                "on_change": lambda e: set_password(e["target"]["value"]),
                "placeholder": "Enter your password",
                "style": get_input_styles(),
            }),
        ),

        html.button({
            "on_click": handle_auth,
            "on_mouse_enter": lambda e: set_login_hover(True),
            "on_mouse_leave": lambda e: set_login_hover(False),
            "style": get_login_button_style(),
            "disabled": loading
        }, "Sign In" if is_login else "Sign Up"),

        html.div({
            "style": {
                "textAlign": "center",
                "marginTop": "1.5rem",
                "paddingTop": "1.5rem",
                "borderTop": f"1px solid {BORDER_COLOR}"
            }
        },
            html.p({
                "style": {
                    "color": TEXT_TERTIARY,
                    "margin": "0 0 1rem 0",
                    "fontSize": "0.9rem"
                }
            }, 
                "Don't have an account? " if is_login else "Already have an account? "
            ),
            html.button({
                "on_click": lambda e: (set_is_login(not is_login), set_error_msg("")),
                "on_mouse_enter": lambda e: set_toggle_hover(True),
                "on_mouse_leave": lambda e: set_toggle_hover(False),
                "style": {
                    "background": "none",
                    "border": "none",
                    "color": "#667eea" if not toggle_hover else "#764ba2",
                    "cursor": "pointer",
                    "fontSize": "0.9rem",
                    "fontWeight": "600",
                    "textDecoration": "underline",
                    "transition": "color 0.2s ease"
                }
            }, "Sign Up" if is_login else "Sign In")
        ),

        error_msg and html.p({
            "style": {
                "color": ERROR,
                "marginTop": "1rem",
                "padding": "0.75rem",
                "background": "#fed7d7",
                "borderRadius": "6px",
                "textAlign": "center",
                "fontSize": "0.9rem"
            }
        }, error_msg),

        loading and html.div({
            "style": {
                "textAlign": "center",
                "marginTop": "1rem",
                "color": TEXT_TERTIARY
            }
        }, "Processing...")
    )