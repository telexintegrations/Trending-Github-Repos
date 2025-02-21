from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", status_code=status.HTTP_200_OK)
def welcome():
    return {"message": "🚀💻 App running Successfully!"}




