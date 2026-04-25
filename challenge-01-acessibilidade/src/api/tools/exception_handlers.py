from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.domain.exceptions import DomainValidationError


def _format_domain_validation_error(error: DomainValidationError) -> dict:
    return {
        "message": error.message,
        "errors": [
            {"location": list(issue.location), "message": issue.message}
            for issue in error.errors
        ],
    }


def _format_validation_error_payload(request: Request, error: Exception) -> dict:
    return {
        "message": "Nao foi possivel validar os dados enviados na requisicao.",
        "path": request.url.path,
        "errors": [
            {
                "location": ["request"],
                "message": str(error),
            }
        ],
    }


def _unprocessable_content(payload: dict) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=payload,
    )


def _build_domain_validation_payload(
    request: Request, error: DomainValidationError
) -> dict:
    formatted_error = _format_domain_validation_error(error)
    return {
        "message": formatted_error["message"],
        "path": request.url.path,
        "errors": formatted_error["errors"],
    }


def validation_error_handler(request: Request, error: ValidationError) -> JSONResponse:
    for validation_error in error.errors():
        wrapped_error = validation_error.get("ctx", {}).get("error")
        if isinstance(wrapped_error, DomainValidationError):
            return _unprocessable_content(
                _build_domain_validation_payload(request, wrapped_error)
            )

    return _unprocessable_content(_format_validation_error_payload(request, error))


def value_error_handler(request: Request, error: ValueError) -> JSONResponse:
    if isinstance(error, DomainValidationError):
        return _unprocessable_content(_build_domain_validation_payload(request, error))

    return _unprocessable_content(_format_validation_error_payload(request, error))


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)
