from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'Airflow',
    'email': ['your.email@domain.com'],
    'start_date': days_ago(1),
    'email_on_failure' : False
}

with DAG(
    dag_id = 'sample-dag',
    default_args = default_args,
    catchup=False,
    max_active_runs = 1,
    schedule_interval = None,
    tags=['sample']
) as dag:

    # define function
    def sample_function():
        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F

        spark = SparkSession.builder \
            .master("local[*]") \
            .appName("airflow_app") \
            .config('spark.executor.memory', '6g') \
            .config('spark.driver.memory', '6g') \
            .config("spark.driver.maxResultSize", "1048MB") \
            .config("spark.port.maxRetries", "100") \
            .getOrCreate()

        df = spark.read.options(inferSchema='true', header='true').csv('/home/airflow/datalake/landing/sample/sample.csv')
        df.show()

    # region BASE TABLES
    sample_task = PythonOperator(
        task_id='sample_task',
        python_callable=sample_function
    )