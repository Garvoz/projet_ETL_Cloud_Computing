import boto3
import json
import pandas as pd
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# On charge les informations stockées dans le fichier ".env".
load_dotenv()

def get_secret() -> dict[str, str]:

    secret_name = "redshiftminiprojet/credentials"
    region_name = "eu-west-3"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']

    # Your code goes here.

    secret_dict = json.loads(secret)

    return secret_dict

def infer_redshift_schema(df: pd.DataFrame, table: str) -> str:
    """
    Cette fonction sert à créer une requête SQL pour créer la table à partir d'un fichier CSV.
    Les types de données de pandas et de Redshift étant différent, on créé un dictionnaire pour le mapping.
    """
    dtype_map = {
        'int64': 'BIGINT',
        'float64': 'FLOAT',
        'object': 'VARCHAR(255)',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP',
    }
    columns = []
    for col, dtype in zip(df.columns, df.dtypes):
        redshift_type = dtype_map.get(str(dtype), 'VARCHAR(255)')
        columns.append(f"{col} {redshift_type}")
    create_table_sql = f"""CREATE TABLE IF NOT EXISTS raw_{table} (
        {',    '.join(columns)}
        );"""
    return create_table_sql

if __name__ == "__main__":
    # On récupère les informations de connexion à Redshift
    secret = get_secret()
    username = secret.get("username")
    password = secret.get("password")
    host = secret.get("host")
    database = "dev"
    port = secret.get("port")

    engine = create_engine(
        f"redshift+psycopg2://{username}:{password}@{host}:{port}/{database}"
    )

    # Liste de toutes les tables 
    tables = ["customers", "items", "orders", "products", "stores", "supplies"]
    
    # Pour chaque table de la liste, on créée une table sur Redshift et on insère les données.
    for table in tables:
        print(f"Table : {table}")            
        df = pd.read_csv(f"https://raw.githubusercontent.com/dsteddy/jaffle_shop_data/main/raw_{table}.csv")

        with engine.connect() as conn:
            create_table_sql = infer_redshift_schema(df, table)
            conn.execute(text(create_table_sql))
            try:
                access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
                secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
                bucket_name = 'bucketminiprojet' # Changez le nom du bucket par le nom que vous avez choisi
                copy_query = f"""
                    COPY raw_{table}
                    FROM 's3://{bucket_name}/raw_{table}.csv'
                    CREDENTIALS 'aws_access_key_id={access_key_id};aws_secret_access_key={secret_access_key}'
                    CSV IGNOREHEADER 1;
                    """
                conn.execute(text(copy_query).execution_options(autocommit=True))
                print(f"Table {table} created")
                print("-"*10)
            except SQLAlchemyError as e:
                print(e)