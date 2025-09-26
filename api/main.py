from fastapi import FastAPI, Depends
from api.routers.users import user_router
from api.auth import oauth2_scheme
app = FastAPI(title="PROGINZH")


# create the instance for the routes

app.include_router(user_router, 
                   prefix="/user", 
                   tags=["user"], 
                   dependencies=[Depends(oauth2_scheme)], 
                   )


@app.get("/")
async def root():
    return {"message": "Hello World"}