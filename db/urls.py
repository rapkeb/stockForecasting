from views import login, logout, register, get_user_purchases, preferences, buy_share


def configure_routes(app):
    app.add_url_rule('/login', 'login', login, methods=["POST"])
    app.add_url_rule('/register', 'register', register, methods=["POST"])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/buy-share', 'buy-share', buy_share, methods=["POST"])
    app.add_url_rule('/preferences', 'preferences', preferences, methods=["GET", "POST"])
    app.add_url_rule('/purchases', 'purchases', get_user_purchases)



