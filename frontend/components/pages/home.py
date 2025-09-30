# frontend/components/pages/home.py
from reactpy import component, html
from frontend.styles.colors import *
from frontend.styles.common import FONT_FAMILY, get_card_styles

@component
def HomePage():
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
                "maxWidth": "1200px",
                "margin": "0 auto"
            }
        },
            html.div({
                "style": {
                    "background": PRIMARY_GRADIENT,
                    "padding": "2.5rem",
                    "borderRadius": "16px",
                    "color": WHITE,
                    "marginBottom": "2rem",
                    "boxShadow": "0 8px 32px rgba(102, 126, 234, 0.3)"
                }
            },
                html.h1({
                    "style": {
                        "margin": "0 0 1rem 0",
                        "fontSize": "2.5rem",
                        "fontWeight": "700"
                    }
                }, "Welcome to Better Health"),
                html.p({
                    "style": {
                        "margin": "0",
                        "fontSize": "1.1rem",
                        "opacity": "0.9",
                        "maxWidth": "600px",
                        "lineHeight": "1.6"
                    }
                }, "Your intelligent healthcare companion. Get personalized health insights, chat with our AI assistant, and manage your wellness journey.")
            ),
            
            html.div({
                "style": {
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))",
                    "gap": "1.5rem",
                    "marginTop": "2rem"
                }
            },
                html.div({
                    "style": {**get_card_styles(), "padding": "2rem"}
                },
                    html.h3({
                        "style": {
                            "margin": "0 0 1rem 0",
                            "color": TEXT_PRIMARY,
                            "fontSize": "1.25rem",
                            "fontWeight": "600"
                        }
                    }, "🩺 Health Monitoring"),
                    html.p({
                        "style": {
                            "margin": "0",
                            "color": TEXT_TERTIARY,
                            "lineHeight": "1.6"
                        }
                    }, "Track your vital signs and health metrics with our AI-powered monitoring system.")
                ),
                
                html.div({
                    "style": {**get_card_styles(), "padding": "2rem"}
                },
                    html.h3({
                        "style": {
                            "margin": "0 0 1rem 0",
                            "color": TEXT_PRIMARY,
                            "fontSize": "1.25rem",
                            "fontWeight": "600"
                        }
                    }, "💊 Medication Tracking"),
                    html.p({
                        "style": {
                            "margin": "0",
                            "color": TEXT_TERTIARY,
                            "lineHeight": "1.6"
                        }
                    }, "Never miss a dose with smart medication reminders and tracking.")
                ),
                
                html.div({
                    "style": {**get_card_styles(), "padding": "2rem"}
                },
                    html.h3({
                        "style": {
                            "margin": "0 0 1rem 0",
                            "color": TEXT_PRIMARY,
                            "fontSize": "1.25rem",
                            "fontWeight": "600"
                        }
                    }, "📈 Progress Analytics"),
                    html.p({
                        "style": {
                            "margin": "0",
                            "color": TEXT_TERTIARY,
                            "lineHeight": "1.6"
                        }
                    }, "View detailed analytics and insights about your health journey over time.")
                )
            )
        )
    )