from decimal import Decimal
import uuid
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestAccountEndpoints:

    def test_craete_account_with_success(self):
        payload = {
            'currency': 'USD',
            'balance': 100.00,
            'is_active': True
        }

        response = client.post("/accounts", json=payload)
        assert response.status_code == 201
        data = response.json()
        print(data)
        assert "account_id" in data

    def test_create_account_with_invalid_data(self):
        payload = {
            'currency': 'MEXICO',
            'balance': 100.00,
            'is_active': True
        }

        response = client.post("/accounts", json=payload)
        assert response.status_code == 422

    def test_get_account_with_success(self):
        payload = {
            'currency': 'USD',
            'balance': 100.00,
            'is_active': True
        }

        response = client.post("/accounts", json=payload)
        assert response.status_code == 201

        account_id = response.json()['account_id']

        response2 = client.get(f"/accounts/{account_id}")
        assert response2.status_code == 200

        data = response2.json()

        assert data["account_id"] == account_id
        assert data["balance"] == '100.0'
        assert data["currency"] == "USD"
        assert data["is_active"] is True

    def test_get_account_invalid_format(self):
        response = client.get("/accounts/invalid-uuid")
        assert response.status_code == 400
        assert response.json()["detail"] == "invalid account_id format!"

    def test_get_account_not_found(self):
        not_found_account_id = str(uuid.uuid4())
        response = client.get(f"/accounts/{not_found_account_id}")
        assert response.status_code == 404



