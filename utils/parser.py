import pandas
import json

def parser(df):
    return json.loads(df.to_json(orient="records"))