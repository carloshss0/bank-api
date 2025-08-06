CREATE TABLE IF NOT EXISTS accounts (
    account_id UUID PRIMARY KEY,
    currency VARCHAR(10),
    balance NUMERIC,
    is_active BOOLEAN
);