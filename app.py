from uuid import UUID
from fastapi import FastAPI, HTTPException, status, Depends
from account.application.create_account import CreateAccountInput, CreateAccountUseCase
from account.application.get_account import GetAccountInput, GetAccountUseCase
from account.infra.account_repository import AccountRepository
from account.web.account_model import AccountCreateRequest, AccountCreateResponse, AccountGetResponse
import os

app = FastAPI()
dsn = os.getenv("DATABASE_DSN", "postgres://user:root@localhost:5432/bank")
repository = AccountRepository(dsn)

@app.post("/accounts", response_model=AccountCreateResponse, status_code=status.HTTP_201_CREATED)
def create_account(account_req: AccountCreateRequest):
    if account_req.account_id is not None:
        try:
            input_data = GetAccountInput(account_id=account_req.account_id)
            use_case = GetAccountUseCase(repository=repository)
            existing = use_case.execute(input_data)
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists!")
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Invalid account_id format: {err}")
        
    
    use_case = CreateAccountUseCase(repository)

    try:

        input = CreateAccountInput(
            currency = account_req.currency,
            balance = account_req.balance,
            is_active= account_req.is_active
        )
        output = use_case.execute(input)

    except Exception as err:
        raise HTTPException(status_code=422, detail=f"Invalid data in the payload: {err}")


    return AccountCreateResponse(
        account_id= output.account_id
    )

@app.get("/accounts/{account_id}", response_model=AccountGetResponse, status_code=status.HTTP_200_OK)
def get_account(account_id: str):
    use_case = GetAccountUseCase(repository)

    try:
        input = GetAccountInput(
            account_id = UUID(account_id)
        )
    except:
        raise HTTPException(status_code=400, detail="invalid account_id format!")

    try:
        output = use_case.execute(input)

        return AccountGetResponse(
            account_id= output.account_id,
            currency= output.currency,
            balance= output.balance,
            is_active= output.is_active,
        )

    except:
        raise HTTPException(status_code=404, detail="account_id not found!")