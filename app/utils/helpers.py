from prophet import Prophet
import pandas as pd

def load_excel_and_split_by_cap(path):
    df = pd.read_csv(path)
    cap_ids = df["Cap_ID"].unique().tolist()
    grouped = {cap: df[df["Cap_ID"] == cap] for cap in cap_ids}
    return grouped, cap_ids

def load_and_prepare_data(df):
    df = df.rename(columns={'Date': 'ds', 'Sales': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], dayfirst=True)
    return df[['ds', 'y']]

def prepare_future(df, periods=30):
    from prophet.make_holidays import make_holidays_df
    model = Prophet()
    model.fit(df)
    return model.make_future_dataframe(periods=periods)
