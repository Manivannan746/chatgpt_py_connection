from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

API_KEY = "349BNWOJW"

@app.middleware("http")
async def check_api(request, call_next):
    key = request.headers.get("api-key")
    if key != API_KEY:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    return await call_next(request)

@app.get("/users")
def get_users():
    return {"message":"WELCOME TO THE WORLD"}

@app.get("/users/{user_id}")
def test(user_id:int):
    if user_id == 1:
        return {"name":"manivannan", "role":"sdet"}
    else:
        return "no_value"

class User(BaseModel):
    name: str
    email: str
    mobile: str

users =[]

@app.post("/user")
def create_user(user: User):
    users.append(user.dict())
    return {"message": "User created successfully {}".format(user.name)}
