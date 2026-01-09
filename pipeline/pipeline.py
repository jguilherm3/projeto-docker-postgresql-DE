import sys
import pandas as pd
print("arguments", sys.argv)

month = int(sys.argv[1])
print(f"Running pipeline for day {month}")

df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
df['month'] = month

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")