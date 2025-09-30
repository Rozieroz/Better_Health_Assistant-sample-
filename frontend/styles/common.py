# frontend/styles/common.py
from . import colors

# Common style patterns
FONT_FAMILY = "'Inter', 'Segoe UI', sans-serif"
LIGHT_BG = "#f7fafc"
PRIMARY_GRADIENT = colors.PRIMARY_GRADIENT


def get_input_styles():
    return {
        "width": "100%",
        "padding": "0.75rem 1rem",
        "border": f"1px solid {colors.BORDER_COLOR}",
        "borderRadius": "8px",
        "fontSize": "0.9rem",
        "transition": "all 0.2s ease",
        "boxSizing": "border-box"
    }

def get_button_styles(variant="primary"):
    base_style = {
        "padding": "0.75rem 1rem",
        "border": "none",
        "borderRadius": "8px",
        "fontSize": "0.9rem",
        "fontWeight": "600",
        "cursor": "pointer",
        "transition": "all 0.2s ease"
    }
    
    if variant == "primary":
        base_style.update({
            "background": colors.PRIMARY_GRADIENT,
            "color": colors.WHITE
        })
    elif variant == "secondary":
        base_style.update({
            "background": colors.WHITE,
            "border": f"1px solid {colors.BORDER_COLOR}",
            "color": colors.TEXT_SECONDARY
        })
    
    return base_style

def get_card_styles():
    return {
        "background": colors.CARD_BG,
        "borderRadius": "12px",
        "boxShadow": colors.CARD_SHADOW,
        "border": f"1px solid {colors.BORDER_COLOR}"
    }