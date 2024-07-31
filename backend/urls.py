from views import buy_share, current_price, preferences, predict
from views import recommendation, company_chart, index, compare_shares, purchases


def configure_routes(app):
    app.add_url_rule('/homepage', 'index', index)
    app.add_url_rule('/company_chart', 'company_chart', company_chart)
    app.add_url_rule('/buy-share', 'buy-share', buy_share, methods=["POST"])
    app.add_url_rule('/current-price', 'current-price', current_price)
    app.add_url_rule('/preferences', 'preferences', preferences, methods=["GET", "POST"])
    app.add_url_rule('/predict', 'predict', predict, methods=["GET"]) 
    app.add_url_rule('/recommendation', 'recommendation', recommendation, methods=["GET"])
    app.add_url_rule('/compare_shares', 'compare_shares', compare_shares)
    app.add_url_rule('/purchases', 'purchases', purchases, methods=["GET"])



