from views import current_price, predict
from views import recommendation, company_chart, index, compare_shares


def configure_routes(app):
    app.add_url_rule('/homepage', 'index', index)
    app.add_url_rule('/company_chart', 'company_chart', company_chart)
    app.add_url_rule('/current-price', 'current-price', current_price)
    app.add_url_rule('/predict', 'predict', predict) 
    app.add_url_rule('/recommendation', 'recommendation', recommendation, methods=["GET"])
    app.add_url_rule('/compare_shares', 'compare_shares', compare_shares)



