# Standard library imports

# Third-party application imports
import botocore.exceptions
from mangum import Mangum
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError


# Local application imports
from routers import router
from exceptions.base import validation_exception_handler, already_exists_exception_handler

app = FastAPI(title='Announcements API', docs_url=None, redoc_url=None)
app.include_router(router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(botocore.exceptions.ClientError, already_exists_exception_handler)
handler = Mangum(app=app)
