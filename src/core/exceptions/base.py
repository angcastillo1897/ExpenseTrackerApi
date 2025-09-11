from pydantic import BaseModel


class BaseExceptionCustom(Exception):
    def __init__(
        self, status_code: int, data: dict | None = None, message: str | None = None
    ) -> None:
        self.__content: dict[str, str] = {}
        if message:
            self.__content.update({"message": message})
        if data:
            self.__content.update(data)
        self.__status_code: int = status_code

    @property
    def respuesta(self):
        return self.__content

    @property
    def status_code(self):
        return self.__status_code


class ResponseException(BaseModel):
    message: str = "Hubo un error al ejecutar el servicio"
