import pytest
from app import app 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_healthz(client):
    # Testing the /healthz endpoint for success.
    response = client.get('/healthz')
    
    assert response.status_code == 200