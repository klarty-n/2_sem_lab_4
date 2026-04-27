from __future__ import annotations
from datetime import datetime
from typing import Any
from src.exceptions import (
    IdError,
    PayloadError,
    PriorityError,
    StatusError,
    StatusTransitionError,
)

allowed_statuses = ("not_started", "in_progress", "completed", "failed")

class IdDescriptor:
    """
    Data descriptor для айди задачи
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> int | IdDescriptor:
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj: Any, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise IdError("айди должен быть целым числом >= 0")
        setattr(obj, self.name, value)


class PriorityDescriptor:
    """
    Data descriptor для приоритета задачи
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> int | PriorityDescriptor:
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj: Any, value: int) -> None:
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise PriorityError("priority должен быть целым числом от 1 до 5")
        setattr(obj, self.name, value)


class StatusDescriptor:
    """
    Data descriptor для статуса задачи
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> str | StatusDescriptor:
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj: Any, value: str) -> None:
        if value not in allowed_statuses:
            raise StatusError(f"status должен быть одним из: {allowed_statuses}")

        # Если статус уже был установлен, проверяем допустимость перехода
        if hasattr(obj, self.name):
            current_status = getattr(obj, self.name)
            if current_status != value and not obj._can_transition(current_status, value):
                raise StatusTransitionError(
                    f"Недопустимый переход статуса: {current_status} -> {value}"
                )
        setattr(obj, self.name, value)


class PayloadDescriptor:
    """
    Data дескриптор для payload задачи
    """

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = f"_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> Any | PayloadDescriptor:
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj: Any, value: Any) -> None:
        if value is None:
            raise PayloadError("payload не может быть None")
        setattr(obj, self.name, value)


class TimeCreatedDescriptor:
    """
    Non-data descriptor для created_at, у дескриптора нет __set__
    """

    def __get__(self, obj: Any, objtype: type | None = None) -> datetime | TimeCreatedDescriptor:
        if obj is None:
            return self
        return getattr(obj, "_created_at", datetime.now())