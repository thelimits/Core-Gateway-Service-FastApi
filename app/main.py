from __future__ import annotations
import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import CustomerController, AccountController
from config.database import engine
import model.CustomerKYC as modelCustomer
import model.CustomerAccount as modelAccount
import model.AccountAdditionalDetails as AccountAdditionalDetails

app = FastAPI()

modelCustomer.Base.metadata.create_all(engine)
modelAccount.Base.metadata.create_all(engine)
AccountAdditionalDetails.Base.metadata.create_all(engine)

prefix = "/demo-service-api"
# api_router = APIRouter(prefix="/demo-service-api")
# app.include_router(api_router)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(CustomerController.router, prefix=prefix)
app.include_router(AccountController.router, prefix=prefix)

@app.get("/")
def root():
    return {"message": "Demo Kit API"}

if __name__=='__main__':
    uvicorn.run(app, port=8080, host="0.0.0.0")