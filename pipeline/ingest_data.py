#!/usr/bin/env python
# coding: utf-8
#!uv add tqdm

import click
import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine

# importar o ORM para levar os dados tratados e fazer a ingestão no Postgres
# vamos agora tratar os tipos de dados que estão incorretos
## procure lembrar bem desse tratamento especificos dos tipos de dados
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='nytaxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year for the data')
@click.option('--month', default=1, type=int, help='Month for the data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')


def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    # create the connection to the Postgres database
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # read the data in chunks
    df_iter = pd.read_csv(
        prefix + 'yellow_tripdata_2021-01.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )
    # ingest the data chunk by chunk
    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
            )
            first=False

        df_chunk.to_sql(
            name=target_table, 
            con=engine, 
            if_exists='append'
        )

if __name__ == '__main__':
    run()