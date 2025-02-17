def stat_card(title, value, color_start, color_end):
    return f"""
    <div style="background: linear-gradient(to right, {color_start}, {color_end}); 
                border-radius: 10px; padding: 20px; text-align: center;">
        <h1 style="color: white; margin: 0;">{value}</h1>
        <p style="color: white; margin: 0;">{title}</p>
    </div>
    """
