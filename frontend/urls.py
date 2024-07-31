from views import company_chart, index, compare_shares, preferences, purchases, logout, login, register, buy_share, current_price, predict, recommendation


def configure_routes(app):
    app.add_url_rule('/', 'login', login)
    app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])
    app.add_url_rule('/register', 'register', register, methods=["GET", "POST"])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/homepage', 'index', index)
    app.add_url_rule('/company_chart', 'company_chart', company_chart)
    app.add_url_rule('/compare_shares', 'compare_shares', compare_shares)
    app.add_url_rule('/preferences', 'preferences', preferences, methods=["GET", "POST"])
    app.add_url_rule('/purchases', 'purchases', purchases, methods=["GET"])
    app.add_url_rule('/buy-share', 'buy-share', buy_share, methods=["POST"])
    app.add_url_rule('/current-price', 'current-price', current_price)
    app.add_url_rule('/recommendation', 'recommendation', recommendation, methods=["GET"])
    app.add_url_rule('/predict', 'predict', predict, methods=["GET"])
