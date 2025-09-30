# frontend/components/pages/profile.py
from reactpy import component, html
from frontend.styles.colors import *
from frontend.styles.common import FONT_FAMILY, get_card_styles

@component
def ProfilePage(user=None):
    return html.div(
        {"style": {
            "padding": "2rem",
            "marginLeft": "280px",
            "minHeight": "100vh",
            "background": LIGHT_BG,
            "fontFamily": FONT_FAMILY
        }},
        html.div({
            "style": {
                "maxWidth": "800px",
                "margin": "0 auto"
            }
        },
            html.div({
                "style": {
                    "background": WHITE,
                    "padding": "2.5rem",
                    "borderRadius": "16px",
                    "boxShadow": CARD_SHADOW,
                    "marginBottom": "2rem"
                }
            },
                html.h1({
                    "style": {
                        "margin": "0 0 2rem 0",
                        "color": TEXT_PRIMARY,
                        "fontSize": "2rem",
                        "fontWeight": "700",
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "1rem"
                    }
                }, 
                    html.span({"style": {"fontSize": "2.5rem"}}, "👤"),
                    "My Profile"
                ),
                
                html.div({
                    "style": {
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                        "gap": "2rem"
                    }
                },
                    html.div(
                        html.h3({
                            "style": {
                                "margin": "0 0 1rem 0",
                                "color": TEXT_SECONDARY,
                                "fontSize": "1rem",
                                "fontWeight": "600",
                                "textTransform": "uppercase",
                                "letterSpacing": "0.05em"
                            }
                        }, "Personal Information"),
                        html.div({
                            "style": {
                                "background": LIGHT_BG,
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "border": f"1px solid {BORDER_COLOR}"
                            }
                        },
                            html.p({
                                "style": {
                                    "margin": "0 0 0.75rem 0",
                                    "display": "flex",
                                    "justifyContent": "space-between"
                                }
                            },
                                html.span({"style": {"color": TEXT_TERTIARY, "fontWeight": "500"}}, "Email:"),
                                html.span({"style": {"color": TEXT_PRIMARY, "fontWeight": "600"}}, user.get("email", "Not set") if user else "Guest User")
                            ),
                            html.p({
                                "style": {
                                    "margin": "0 0 0.75rem 0",
                                    "display": "flex",
                                    "justifyContent": "space-between"
                                }
                            },
                                html.span({"style": {"color": TEXT_TERTIARY, "fontWeight": "500"}}, "Name:"),
                                html.span({"style": {"color": TEXT_PRIMARY, "fontWeight": "600"}}, user.get("name", "Not set") if user else "Guest User")
                            ),
                            html.p({
                                "style": {
                                    "margin": "0",
                                    "display": "flex",
                                    "justifyContent": "space-between"
                                }
                            },
                                html.span({"style": {"color": TEXT_TERTIARY, "fontWeight": "500"}}, "Status:"),
                                html.span({
                                    "style": {
                                        "color": SUCCESS,
                                        "fontWeight": "600",
                                        "background": "#f0fff4",
                                        "padding": "0.25rem 0.75rem",
                                        "borderRadius": "12px",
                                        "fontSize": "0.8rem"
                                    }
                                }, "Active")
                            )
                        )
                    ),
                    
                    html.div(
                        html.h3({
                            "style": {
                                "margin": "0 0 1rem 0",
                                "color": TEXT_SECONDARY,
                                "fontSize": "1rem",
                                "fontWeight": "600",
                                "textTransform": "uppercase",
                                "letterSpacing": "0.05em"
                            }
                        }, "Account Settings"),
                        html.div({
                            "style": {
                                "background": LIGHT_BG,
                                "padding": "1.5rem",
                                "borderRadius": "8px",
                                "border": f"1px solid {BORDER_COLOR}"
                            }
                        },
                            html.button({
                                "style": {
                                    "width": "100%",
                                    "padding": "0.75rem",
                                    "marginBottom": "0.75rem",
                                    "background": WHITE,
                                    "border": f"1px solid {BORDER_COLOR}",
                                    "borderRadius": "6px",
                                    "color": TEXT_SECONDARY,
                                    "cursor": "pointer",
                                    "fontWeight": "500",
                                    "transition": "all 0.2s ease"
                                },
                                "on_mouse_enter": lambda e: e.target.update({"style": {"borderColor": "#667eea", "color": "#667eea"}}),
                                "on_mouse_leave": lambda e: e.target.update({"style": {"borderColor": BORDER_COLOR, "color": TEXT_SECONDARY}})
                            }, "Edit Profile"),
                            html.button({
                                "style": {
                                    "width": "100%",
                                    "padding": "0.75rem",
                                    "marginBottom": "0.75rem",
                                    "background": WHITE,
                                    "border": f"1px solid {BORDER_COLOR}",
                                    "borderRadius": "6px",
                                    "color": TEXT_SECONDARY,
                                    "cursor": "pointer",
                                    "fontWeight": "500",
                                    "transition": "all 0.2s ease"
                                },
                                "on_mouse_enter": lambda e: e.target.update({"style": {"borderColor": "#667eea", "color": "#667eea"}}),
                                "on_mouse_leave": lambda e: e.target.update({"style": {"borderColor": BORDER_COLOR, "color": TEXT_SECONDARY}})
                            }, "Privacy Settings"),
                            html.button({
                                "style": {
                                    "width": "100%",
                                    "padding": "0.75rem",
                                    "background": "#fed7d7",
                                    "border": "1px solid #feb2b2",
                                    "borderRadius": "6px",
                                    "color": "#c53030",
                                    "cursor": "pointer",
                                    "fontWeight": "500",
                                    "transition": "all 0.2s ease"
                                },
                                "on_mouse_enter": lambda e: e.target.update({"style": {"background": "#feb2b2", "borderColor": "#fc8181"}}),
                                "on_mouse_leave": lambda e: e.target.update({"style": {"background": "#fed7d7", "borderColor": "#feb2b2"}})
                            }, "Delete Account")
                        )
                    )
                )
            )
        )
    )