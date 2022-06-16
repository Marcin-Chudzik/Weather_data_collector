from datetime import datetime, timedelta
from textwrap import dedent

# DAG object
from airflow import DAG

# Operator
from airflow.operators.bash import BashOperator

with DAG(
    'test',
    # args to each operator
    default_args={
        'depends_on_past': False,
        'email': ['chmc2001@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    description='Just a test of airflow DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 6, 16),
    catchup=False,
    tags=['example'],
) as dag:
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3
    )
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7) }}"
    {% endfor %}    
    """
    )

    t3 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
    )

    t1.doc_md = dedent(
        """\
    #### Task Documentation
    """
    )

    dag.doc_md = __doc__
    dag.doc_md = """
    --- Task Documentation ---
    Here is a short documentation of my test DAG.
    """

t1 >> [t2, t3]
