from views import company_chart, index, compare_shares, preferences, purchases, logout, login, register


def configure_routes(app):
    app.add_url_rule('/', 'login', login)
    app.add_url_rule('/login', 'login', login)
    app.add_url_rule('/register', 'register', register)
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/homepage', 'index', index)
    app.add_url_rule('/company', 'company_chart', company_chart)
    app.add_url_rule('/compare_shares', 'compare_shares', compare_shares)
    app.add_url_rule('/preferences', 'preferences', preferences, methods=["GET"])
    app.add_url_rule('/purchases', 'purchases', purchases)
