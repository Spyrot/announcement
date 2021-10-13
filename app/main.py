# Standard library imports

# Third-party application imports
import uvicorn
from fastapi import FastAPI
from mangum import Mangum

# Local application imports
from routers import router

app = FastAPI(title='Announcements API', openapi_url="/prod/openapi.json")
app.include_router(router)
handler = Mangum(app=app)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)