from prophet import Prophet

class ForecastModel:
    def __init__(self):
        self.model = None

    def predict(self, df, future):
        self.model = Prophet()
        self.model.fit(df)
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
