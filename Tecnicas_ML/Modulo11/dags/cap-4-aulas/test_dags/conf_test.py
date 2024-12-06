import pytest
from airflow.models import DagBag

# Fixture do pytest para carregar a instância do DagBag, que gerencia as DAGs no Airflow
@pytest.fixture(scope="session")
def dagbag():
    return DagBag()
