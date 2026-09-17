import json
import urllib.parse
from datetime import datetime, timezone

import boto3

BUCKET = "xideralaws-curso-proyecto-alan"

s3 = boto3.client(
    "s3",
    region_name="us-west-1"
)


def lambda_handler(event, context):

    for record in event.get("Records", []):

        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        if not key.endswith(".parquet"):
            print(f"Ignorado (no parquet): {key}")
            continue

        parts = key.split("/")

        # raw_data/{year}/{month}/{filename}.parquet
        if len(parts) != 4:
            print(f"Ignorado (ruta inesperada): {key}")
            continue

        year = parts[1]
        month = parts[2]
        filename = parts[3]

        # yellow_tripdata_2024-01.parquet
        taxi_type = filename.split("_tripdata_")[0]

        size = s3.head_object(
            Bucket=BUCKET,
            Key=key
        )["ContentLength"]

        payload = {
            "s3_bucket": BUCKET,
            "s3_key": key,
            "taxi_type": taxi_type,
            "file_year": int(year),
            "file_month": int(month),
            "file_size_bytes": size,
            "num_rows": None,
            "registered_by": "lambda-taxi-metadata",
            "registered_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        out_key = (
            f"metadata/year={year}/month={month}/"
            f"{filename.replace('.parquet', '.json')}"
        )

        s3.put_object(
            Bucket=BUCKET,
            Key=out_key,
            Body=json.dumps(
                payload,
                indent=2
            ).encode("utf-8"),
            ContentType="application/json"
        )

        print(f"OK -> {out_key}")

    return {
        "statusCode": 200,
        "body": "procesado"
    }
