from sqlalchemy.orm import Session
from starlette.requests import Request


def get_db(request: Request) -> Session:
    """
    Get DB session.
    """
    session_local = request.app.state.session
    with session_local() as session:
        try:
            yield session
        finally:
            session.close()
