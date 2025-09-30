# frontend/components/pages/chat.py
from reactpy import component, html, hooks
from frontend.styles.colors import *
from frontend.styles.common import FONT_FAMILY, get_input_styles, get_button_styles, get_card_styles
import json
import datetime


@component
def ChatPage(token=None, user=None):
    user_input, set_user_input = hooks.use_state("")
    chat_log, set_chat_log = hooks.use_state([])
    loading, set_loading = hooks.use_state(False)
    conversation_history, set_conversation_history = hooks.use_state([])

    async def send_message(event):
        if not user_input.strip() or loading:
            return

        # Add user message to chat log immediately
        user_message = {
            "type": "user",
            "content": user_input,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        set_chat_log([*chat_log, user_message])
        set_user_input("")
        set_loading(True)

        try:
            # Use mock endpoint for now since we're avoiding OpenAI
            response = await fetch(
                "http://localhost:8000/ai/chat/mock",
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}" if token else ""
                },
                body=json.dumps({
                    "message": user_input,
                    "conversation_history": conversation_history
                })
            )
            
            if response.status == 200:
                data = await response.json()
                ai_message = {
                    "type": "ai",
                    "content": data["response"],
                    "timestamp": data.get("timestamp", datetime.datetime.now().isoformat())
                }
                
                # Update conversation history for context
                set_conversation_history([
                    *conversation_history[-4:],  # Keep last 4 messages for context
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": data["response"]}
                ])
                
                set_chat_log(chat_log + [user_message, ai_message])
            else:
                error_data = await response.json()
                error_message = {
                    "type": "error",
                    "content": f"Error: {error_data.get('detail', 'Failed to get response')}",
                    "timestamp": datetime.datetime.now().isoformat()
                }
                set_chat_log(chat_log + [user_message, error_message])
                
        except Exception as e:
            error_message = {
                "type": "error",
                "content": f"Network error: {str(e)}",
                "timestamp": datetime.datetime.now().isoformat()
            }
            set_chat_log(chat_log + [user_message, error_message])
        finally:
            set_loading(False)

    def format_timestamp(timestamp):
        try:
            dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%H:%M")
        except:
            return ""

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
                "margin": "0 auto",
                "background": WHITE,
                "borderRadius": "16px",
                "boxShadow": CARD_SHADOW,
                "overflow": "hidden",
                "height": "80vh",
                "display": "flex",
                "flexDirection": "column"
            }
        },
            html.div({
                "style": {
                    "background": PRIMARY_GRADIENT,
                    "padding": "1.5rem 2rem",
                    "color": WHITE
                }
            },
                html.h1({
                    "style": {
                        "margin": "0",
                        "fontSize": "1.5rem",
                        "fontWeight": "600"
                    }
                }, "💬 Better Health AI Assistant"),
                html.p({
                    "style": {
                        "margin": "0.5rem 0 0 0",
                        "opacity": "0.9",
                        "fontSize": "0.9rem"
                    }
                }, f"Hello {user.get('name', 'User') if user else 'User'}! Ask me anything about health and wellness")
            ),
            
            html.div({
                "style": {
                    "flex": "1",
                    "padding": "1.5rem",
                    "overflowY": "auto",
                    "background": "#fafbfc",
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "1rem"
                }},
                # Welcome message if no chat history
                (not chat_log) and html.div({
                    "style": {
                        "textAlign": "center",
                        "padding": "2rem",
                        "color": TEXT_TERTIARY
                    }
                },
                    html.h3({"style": {"marginBottom": "1rem"}}, "👋 Welcome to Better Health AI Chat"),
                    html.p({"style": {"marginBottom": "0.5rem"}}, "I'm here to help with general health information and wellness tips."),
                    html.p({"style": {"marginBottom": "0.5rem"}}, "💡 You can ask me about:"),
                    html.ul({"style": {"textAlign": "left", "display": "inline-block"}},
                        html.li("Healthy lifestyle tips"),
                        html.li("Exercise and nutrition"),
                        html.li("Sleep and mental wellness"),
                        html.li("General health questions")
                    ),
                    html.p({
                        "style": {
                            "marginTop": "1rem",
                            "padding": "0.75rem",
                            "background": "#fff5f5",
                            "borderRadius": "8px",
                            "fontSize": "0.9rem",
                            "color": "#c53030"
                        }
                    }, "⚠️ Remember: I'm an AI assistant, not a doctor. Always consult healthcare professionals for medical advice.")
                ),
                
                # Chat messages
                [html.div({
                    "key": f"msg-{index}",
                    "style": {
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "flex-start" if msg["type"] == "ai" else "flex-end",
                        "gap": "0.25rem"
                    }
                },
                    html.div({
                        "style": {
                            "padding": "1rem 1.25rem",
                            "borderRadius": "12px",
                            "background": "#667eea" if msg["type"] == "ai" else WHITE,
                            "color": WHITE if msg["type"] == "ai" else TEXT_PRIMARY,
                            "border": f"1px solid {BORDER_COLOR}" if msg["type"] == "user" else "none",
                            "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.06)" if msg["type"] == "user" else "0 2px 8px rgba(102, 126, 234, 0.3)",
                            "maxWidth": "80%",
                            "position": "relative"
                        }
                    }, 
                        html.div({
                            "style": {
                                "fontWeight": "600",
                                "marginBottom": "0.25rem",
                                "fontSize": "0.8rem",
                                "opacity": "0.8"
                            }
                        }, "AI Assistant" if msg["type"] == "ai" else "You"),
                        html.div({
                            "style": {
                                "fontSize": "0.9rem",
                                "lineHeight": "1.5",
                                "whiteSpace": "pre-wrap"
                            }
                        }, msg["content"]),
                        html.div({
                            "style": {
                                "fontSize": "0.7rem",
                                "opacity": "0.6",
                                "marginTop": "0.5rem",
                                "textAlign": "right"
                            }
                        }, format_timestamp(msg["timestamp"]))
                    )
                ) for index, msg in enumerate(chat_log)],
                
                # Loading indicator
                loading and html.div({
                    "style": {
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "0.5rem",
                        "padding": "1rem",
                        "color": TEXT_TERTIARY,
                        "fontSize": "0.9rem"
                    }
                },
                    html.div({
                        "style": {
                            "width": "12px",
                            "height": "12px",
                            "border": "2px solid #e2e8f0",
                            "borderTop": "2px solid #667eea",
                            "borderRadius": "50%",
                            "animation": "spin 1s linear infinite"
                        }
                    }),
                    "AI is thinking..."
                )
            ),
            
            html.div({
                "style": {
                    "padding": "1.5rem",
                    "borderTop": f"1px solid {BORDER_COLOR}",
                    "background": WHITE
                }
            },
                html.div({
                    "style": {
                        "display": "flex",
                        "gap": "1rem"
                    }
                },
                    html.input({
                        "type": "text",
                        "value": user_input,
                        "on_change": lambda e: set_user_input(e["target"]["value"]),
                        "placeholder": "Type your health question...",
                        "style": {**get_input_styles(), "flex": "1"},
                        "on_focus": lambda e: e.target.update({
                            "style": {**get_input_styles(), "flex": "1", "border": f"1px solid #667eea", "outline": "none", "boxShadow": FOCUS_SHADOW}
                        }),
                        "on_blur": lambda e: e.target.update({
                            "style": {**get_input_styles(), "flex": "1", "outline": "none"}
                        }),
                        "on_key_press": lambda e: e["key"] == "Enter" and send_message(e),
                        "disabled": loading
                    }),
                    html.button({
                        "on_click": send_message,
                        "style": get_button_styles("primary"),
                        "on_mouse_enter": lambda e: not loading and e.target.update({
                            "style": {**get_button_styles("primary"), "transform": "translateY(-1px)", "boxShadow": HOVER_SHADOW}
                        }),
                        "on_mouse_leave": lambda e: not loading and e.target.update({
                            "style": {**get_button_styles("primary"), "transform": "translateY(0)", "boxShadow": "none"}
                        }),
                        "disabled": loading or not user_input.strip()
                    }, "Send" if not loading else "Sending...")
                ),
                html.p({
                    "style": {
                        "margin": "0.5rem 0 0 0",
                        "color": TEXT_TERTIARY,
                        "fontSize": "0.8rem",
                        "textAlign": "center"
                    }
                }, "💡 Press Enter to send your message")
            )
        )
    )