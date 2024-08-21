from views import login, logout, register, get_user_purchases, preferences, buy_share, is_logged_in, write_user_interaction, get_login_interactions, get_shares_interactions, get_buy_interactions, is_admin


def configure_routes(app):
    app.add_url_rule('/login', 'login', login, methods=["POST"])
    app.add_url_rule('/register', 'register', register, methods=["POST"])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/buy-share', 'buy-share', buy_share, methods=["POST"])
    app.add_url_rule('/preferences', 'preferences', preferences, methods=["GET", "POST"])
    app.add_url_rule('/purchases', 'purchases', get_user_purchases)
    app.add_url_rule('/auth', 'auth', is_logged_in)
    app.add_url_rule('/admin', 'admin', is_admin)
    app.add_url_rule('/write_user_interaction', 'write_user_interaction', write_user_interaction, methods=["POST"])
    app.add_url_rule('/buy_interactions', 'buy_interactions', get_buy_interactions)
    app.add_url_rule('/shares_interactions', 'shares_interactions', get_shares_interactions)
    app.add_url_rule('/login_interactions', 'login_interactions', get_login_interactions)



