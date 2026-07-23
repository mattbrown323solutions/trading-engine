from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_database_session
from app.models.event import SystemEvent
from app.schemas.event import SystemEventCreate, SystemEventRead


router = APIRouter(
    prefix="/events",
    tags=["events"],
)

DatabaseSession = Annotated[
    Session,
    Depends(get_database_session),
]


@router.post(
    "",
    response_model=SystemEventRead,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    payload: SystemEventCreate,
    session: DatabaseSession,
) -> SystemEvent:
    event = SystemEvent(
        event_type=payload.event_type,
        message=payload.message,
    )

    session.add(event)

    try:
        session.commit()
        session.refresh(event)
    except SQLAlchemyError as exc:
        session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create system event",
        ) from exc

    return event


@router.get(
    "",
    response_model=list[SystemEventRead],
)
def list_events(
    session: DatabaseSession,
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 20,
) -> list[SystemEvent]:
    statement = (
        select(SystemEvent)
        .order_by(
            SystemEvent.created_at.desc(),
            SystemEvent.id.desc(),
        )
        .limit(limit)
    )

    return list(session.scalars(statement))
