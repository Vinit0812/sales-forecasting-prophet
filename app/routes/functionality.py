from flask import Blueprint
from flask_restful import Api
from app.routes.forecast_routes import Forecast, CapIDs

forecast_api_bp = Blueprint('forecast_api_bp', __name__)
api = Api(forecast_api_bp)

api.add_resource(Forecast, '/forecast/<string:cap_id>')
api.add_resource(CapIDs, '/cap_ids')
