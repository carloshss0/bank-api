# 💰 Mini Bank API Challenge

A backend challenge to build a REST API application for managing bank accounts and money transfers.

## 🎯 Objective

Create a simple banking system with basic features:
- Account creation
- Balance checks
- Money transfers between accounts
- Transaction tracking

This challenge helps sharpen backend skills in API design, validation, data persistence, and transactional logic.

---

## 🧩 Features to Implement

### 📘 Accounts

- `POST /accounts`
  - Create a new account.
  - Example body:
    ```json
    {
      "currency": "USD",
      "balance": 500.0,
      "is_active": true,
    }
    ```

- `GET /accounts/{id}`
  - Get details for a specific account.

- `GET /accounts`
  - List all accounts.

---

### 💸 Transactions

- `POST /transactions`
  - Transfer money from one account to another.
  - Request body:
    ```json
    {
      "from_account_id": 1,
      "to_account_id": 2,
      "amount": 100.0
    }
    ```

  - Validations:
    - Both accounts must exist.
    - `from_account` must have sufficient funds.
    - Record the transaction with:
      - Unique transaction ID
      - Timestamp
      - Status (`completed`, `failed`, etc.)

- `GET /transactions`
  - List all transactions.

- `GET /accounts/{id}/transactions`
  - Get all transactions for a specific account (incoming and outgoing).

---

### 💰 Balance

- `GET /accounts/{id}/balance`
  - Return the current balance of the given account.

---

## 🧪 Requirements

- ✅ Use **FastAPI** (preferred) or Flask
- ✅ Use **Postgres** as the database
- ✅ Use **Pydantic** models for validation and serialization
- ✅ Handle errors and validations (e.g., account not found, insufficient funds)
- ✅ Write at least **5 tests** using `pytest`
- ✅ Use `datetime` or `ISO 8601` format for timestamps
- ✅ Use SQL transactions for atomic transfers

---

## 🚀 Bonus (Optional)

- [ ] Add the ability to **reverse** a transaction
- [ ] Add **account locking** to avoid race conditions (simulate concurrency)
- [ ] Add **pagination** to `/transactions`
- [ ] Dockerize the app for easy startup

---


