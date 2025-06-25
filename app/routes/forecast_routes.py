from flask import request
from flask_restful import Resource
from app.model.forecast_model import ForecastModel
from app.utils.helpers import load_excel_and_split_by_cap, load_and_prepare_data, prepare_future
import pandas as pd

grouped_data, cap_ids = load_excel_and_split_by_cap("app/sample_data/sales_data.csv")
forecast_model = ForecastModel()


class Forecast(Resource):
    def get(self, cap_id):
        if cap_id not in grouped_data:
            return {"error": f"Cap_ID '{cap_id}' not found"}, 404

        df = grouped_data[cap_id]
        df = load_and_prepare_data(df)
        future = prepare_future(df)
        forecast = forecast_model.predict(df, future)

        forecast['ds'] = forecast['ds'].astype(str)
        return forecast.to_dict(orient='records'), 200

    def post(self, cap_id):
        """Add new sales data for a cap_id"""
        data = request.get_json()
        if not data or not all(k in data for k in ('Date', 'Sales')):
            return {"error": "Missing 'Date' or 'Sales' in payload"}, 400

        new_entry = pd.DataFrame([data])
        if cap_id in grouped_data:
            grouped_data[cap_id] = pd.concat([grouped_data[cap_id], new_entry], ignore_index=True)
        else:
            grouped_data[cap_id] = new_entry
            cap_ids.append(cap_id)

        return {"message": f"Data added for Cap_ID '{cap_id}'"}, 201

    def put(self, cap_id):
        """Update the last sales entry for a given Cap_ID"""
        if cap_id not in grouped_data:
            return {"error": f"Cap_ID '{cap_id}' not found"}, 404

        data = request.get_json()
        if not data or not all(k in data for k in ('Date', 'Sales')):
            return {"error": "Missing 'Date' or 'Sales' in payload"}, 400

        grouped_data[cap_id].iloc[-1] = data
        return {"message": f"Last entry updated for Cap_ID '{cap_id}'"}, 200

    def delete(self, cap_id):
        """Delete all data for a given Cap_ID"""
        if cap_id not in grouped_data:
            return {"error": f"Cap_ID '{cap_id}' not found"}, 404

        del grouped_data[cap_id]
        cap_ids.remove(cap_id)
        return {"message": f"All data for Cap_ID '{cap_id}' deleted"}, 200


class CapIDs(Resource):
    def get(self):
        """List all available Cap_IDs"""
        return {"cap_ids": cap_ids}

    def post(self):
        """Add a new Cap_ID (without sales data)"""
        data = request.get_json()
        new_cap_id = data.get("Cap_ID")
        if not new_cap_id:
            return {"error": "Cap_ID is required"}, 400
        if new_cap_id in cap_ids:
            return {"error": f"Cap_ID '{new_cap_id}' already exists"}, 400

        cap_ids.append(new_cap_id)
        grouped_data[new_cap_id] = pd.DataFrame(columns=["Date", "Sales"])
        return {"message": f"Cap_ID '{new_cap_id}' added"}, 201

    def put(self):
        """Rename an existing Cap_ID"""
        data = request.get_json()
        old_cap_id = data.get("old_Cap_ID")
        new_cap_id = data.get("new_Cap_ID")

        if not old_cap_id or not new_cap_id:
            return {"error": "Both 'old_Cap_ID' and 'new_Cap_ID' are required"}, 400
        if old_cap_id not in cap_ids:
            return {"error": f"Cap_ID '{old_cap_id}' not found"}, 404
        if new_cap_id in cap_ids:
            return {"error": f"Cap_ID '{new_cap_id}' already exists"}, 400

        cap_ids[cap_ids.index(old_cap_id)] = new_cap_id
        grouped_data[new_cap_id] = grouped_data.pop(old_cap_id)

        return {"message": f"Cap_ID renamed from '{old_cap_id}' to '{new_cap_id}'"}, 200

    def delete(self):
        """Delete a Cap_ID (and its data)"""
        data = request.get_json()
        cap_id = data.get("Cap_ID")
        if not cap_id:
            return {"error": "Cap_ID is required"}, 400
        if cap_id not in cap_ids:
            return {"error": f"Cap_ID '{cap_id}' not found"}, 404

        cap_ids.remove(cap_id)
        grouped_data.pop(cap_id, None)
        return {"message": f"Cap_ID '{cap_id}' deleted"}, 200
