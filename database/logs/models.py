from pydantic import BaseModel, Field


class Log(BaseModel):
    """Model representing a log entry."""
    log_id: str = Field(..., description="Уникальный идентификатор лога")
    timestamp: str = Field(..., description="Временная метка события")
    user_id: int = Field(..., description="Идентификатор пользователя, связанного с событием")
    action: str = Field(..., description="Описание действия или события")
