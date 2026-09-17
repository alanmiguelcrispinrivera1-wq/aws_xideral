"""
Backfill de metadata para objetos existentes en S3
====================================================

Objetivo
--------
Generar la metadata (mismo formato que produce la Lambda `alan`) para los
archivos Parquet que ya estaban en raw_data/ antes de crear la Lambda. El
trigger de S3 solo se dispara sobre objetos nuevos, así que estos 117 objetos
existentes nunca generaron su JSON en metadata/.

Prerrequisitos:
- boto3 configurado en este entorno (EC2) con permisos de lectura sobre
  raw_data/ y escritura sobre metadata/ en el bucket.
- Confirmar que la región del cliente (us-west-1) coincide con la del bucket.

Salida esperada:
Un JSON por cada objeto Parquet en raw_data/, guardado en
metadata/year={year}/month={month}/{archivo}.json, con el mismo esquema que
usa la Lambda (taxi_type, file_size_bytes, num_rows: null, etc.), pero con
registered_by: "backfill-taxi-metadata" para distinguirlo de los registros
que genera la Lambda en tiempo real.
"""

import json
from datetime import datetime, timezone

import boto3

BUCKET = "xideralaws-curso-proyecto-alan"
PREFIX = "raw_data/"

# Inicializamos el cliente
s3 = boto3.client("s3", region_name="us-west-1")


# Función de procesamiento por objeto
# ------------------------------------
# Toma la key y el tamaño de un objeto de S3 (ya obtenidos por list_objects_v2)
# y genera su JSON de metadata, igual que lo hace la Lambda.
#
# Decisiones de diseño:
# - Reutiliza exactamente la misma lógica de parseo que la Lambda
#   (raw_data/{year}/{month}/{filename}.parquet, tipo derivado del nombre del
#   archivo) para que ambos caminos produzcan el mismo esquema.
# - No usa head_object para obtener el tamaño: list_objects_v2 ya lo trae en
#   cada resultado, así que nos ahorramos 117 llamadas extra a la API.
# - registered_by queda como "backfill-taxi-metadata" en vez de
#   "lambda-taxi-metadata", para poder distinguir después en RDS qué registros
#   vinieron del backfill inicial y cuáles del trigger en tiempo real.
# - Es idempotente: si se vuelve a correr, sobrescribe el mismo JSON con la
#   misma key determinística, sin duplicar nada.
def procesar_objeto(key, size):
    parts = key.split("/")

    # raw_data/{year}/{month}/{filename}.parquet
    if len(parts) != 4:
        print(f"Ignorado (ruta inesperada): {key}")
        return False

    year, month, filename = parts[1], parts[2], parts[3]

    if not filename.endswith(".parquet"):
        print(f"Ignorado (no parquet): {key}")
        return False

    # yellow_tripdata_2024-01.parquet
    taxi_type = filename.split("_tripdata_")[0]

    payload = {
        "s3_bucket": BUCKET,
        "s3_key": key,
        "taxi_type": taxi_type,
        "file_year": int(year),
        "file_month": int(month),
        "file_size_bytes": size,
        "num_rows": None,
        "registered_by": "backfill-taxi-metadata",
        "registered_at": datetime.now(timezone.utc).isoformat()
    }

    out_key = (
        f"metadata/year={year}/month={month}/"
        f"{filename.replace('.parquet', '.json')}"
    )

    s3.put_object(
        Bucket=BUCKET,
        Key=out_key,
        Body=json.dumps(payload, indent=2).encode("utf-8"),
        ContentType="application/json"
    )

    print(f"OK -> {out_key}")
    return True


# Ejecución: backfill de todos los objetos en raw_data/
# -------------------------------------------------------
# Recorre todo el prefijo raw_data/ con un paginador (por si en el futuro hay
# más de 1000 objetos, el límite de una sola llamada a list_objects_v2) y
# llama a procesar_objeto por cada Parquet encontrado.
#
# Antes de correr este script: si dejaste el archivo de prueba
# raw_data/2099/01/test_tripdata_2099-01.parquet de la validación del
# trigger, bórralo primero.
#
# Salida esperada: 117 líneas "OK -> metadata/..." y el resumen final
# "Backfill completado: 117/117 objetos procesados".
def main():
    paginator = s3.get_paginator("list_objects_v2")
    total = 0
    procesados = 0

    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if not key.endswith(".parquet"):
                continue
            total += 1
            if procesar_objeto(key, obj["Size"]):
                procesados += 1

    print(f"\nBackfill completado: {procesados}/{total} objetos procesados")


if __name__ == "__main__":
    main()
