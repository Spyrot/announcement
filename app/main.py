# Standard library imports

# Third-party application imports
from fastapi import FastAPI
from mangum import Mangum

# Local application imports
from routers import router

app = FastAPI(title='Announcements API')
app.include_router(router)
handler = Mangum(app=app)
