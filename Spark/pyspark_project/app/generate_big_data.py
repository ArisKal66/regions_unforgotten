import pandas as pd
import numpy as np

N = 10000
num_users = 1000
record_starting_date = '2019-01-01'

df = pd.DataFrame({
    "transaction_id" : range(1,N+1),
    "user_id": np.random.randint(1, num_users+1, size=N),
    "amount": np.random.uniform(1.0, 1000.0, size=N).round(2),
    "channel": np.random.choice(['online', 'in-store', 'mobile',"b2b"], size=N, p=[0.4, 0.3, 0.2, 0.1]),
    "timestamp": pd.date_range(start=record_starting_date, periods=N, freq='T')
})

df.to_csv("D:/prOJ/regions_unforgotten/Spark/pyspark_project/data/big_data.csv", index=False, sep=';')
print("Big data CSV file generated: big_data.csv")