# frontend/components/sidebar.py
from reactpy import component, html
from frontend.styles.colors import *
from frontend.styles.common import FONT_FAMILY

@component
def Sidebar(current_page, set_page, user):
    def nav_item(label, page, icon):
        is_active = current_page == page
        active_style = {
            "background": PRIMARY_GRADIENT,
            "color": WHITE,
            "boxShadow": "0 2px 8px rgba(102, 126, 234, 0.3)"
        } if is_active else {
            "color": TEXT_SECONDARY,
            "background": "transparent"
        }
        
        return html.li(
            {"style": {"listStyle": "none", "marginBottom": "0.5rem"}},
            html.button({
                "on_click": lambda e, p=page: set_page(p),
                "style": {
                    "width": "100%",
                    "padding": "0.75rem 1rem",
                    "textAlign": "left",
                    "border": "none",
                    "background": "none",
                    "cursor": "pointer",
                    "borderRadius": "8px",
                    "fontSize": "0.9rem",
                    "fontWeight": "500",
                    "transition": "all 0.2s ease",
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "0.75rem",
                    **active_style,
                },
                "on_mouse_enter": lambda e: not is_active and e.target.update({
                    "style": {"background": LIGHT_BG, "color": TEXT_PRIMARY}
                }),
                "on_mouse_leave": lambda e: not is_active and e.target.update({
                    "style": {"background": "transparent", "color": TEXT_SECONDARY}
                })
            }, 
                html.span({"style": {"fontSize": "1.1rem"}}, icon),
                label
            ),
        )

    return html.nav(
        {"style": {
            "padding": "1.5rem 1rem",
            "borderRight": f"1px solid {BORDER_COLOR}",
            "height": "100vh",
            "width": "280px",
            "background": WHITE,
            "boxShadow": "2px 0 8px rgba(0, 0, 0, 0.04)",
            "fontFamily": FONT_FAMILY,
            "position": "fixed",
            "left": 0,
            "top": 0
        }},
        html.div(
            {"style": {
                "display": "flex",
                "alignItems": "center",
                "gap": "0.75rem",
                "marginBottom": "2rem",
                "padding": "0 0.5rem"
            }},
            html.div({
                "style": {
                    "background": PRIMARY_GRADIENT,
                    "width": "40px",
                    "height": "40px",
                    "borderRadius": "10px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "color": WHITE,
                    "fontSize": "1.2rem"
                }
            }, "🏥"),
            html.div(
                html.h3({
                    "style": {
                        "margin": "0",
                        "color": TEXT_PRIMARY,
                        "fontWeight": "700",
                        "fontSize": "1.25rem"
                    }
                }, "Better Health AI"),
                html.p({
                    "style": {
                        "margin": "0",
                        "color": TEXT_TERTIARY,
                        "fontSize": "0.8rem",
                        "fontWeight": "500"
                    }
                }, user.get("name", "User") if user else "Medical Assistant")
            )
        ),

        html.ul({"style": {"padding": 0, "margin": 0}},
            nav_item("Dashboard", "Home", "📊"),
            nav_item("AI Chat", "Chat", "💬"),
            nav_item("My Profile", "Profile", "👤"),
            nav_item("Logout", "Logout", "🚪"),
        ),
        
        html.div({
            "style": {
                "position": "absolute",
                "bottom": "2rem",
                "left": "1rem",
                "right": "1rem",
                "padding": "1rem",
                "background": LIGHT_BG,
                "borderRadius": "8px",
                "border": f"1px solid {BORDER_COLOR}"
            }
        },
            html.p({
                "style": {
                    "margin": "0 0 0.5rem 0",
                    "color": TEXT_PRIMARY,
                    "fontSize": "0.9rem",
                    "fontWeight": "600"
                }
            }, "Need Help?"),
            html.p({
                "style": {
                    "margin": "0",
                    "color": TEXT_TERTIARY,
                    "fontSize": "0.8rem",
                    "lineHeight": "1.4"
                }
            }, "Our AI assistant is available 24/7 to answer your health questions.")
        )
    )