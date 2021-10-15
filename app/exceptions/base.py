# Standard library imports

# Third-party application imports
import botocore.exceptions
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Local application imports


def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


def already_exists_exception_handler(_: Request, exc: botocore.exceptions.ClientError):
    # It's not a good practise to return DB errors to request client, but good practise will require to create
    # additional layer with errors handling
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({"detail": exc.response["Error"]}),
    )
