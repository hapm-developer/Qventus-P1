# Import all the models, so that Base has them before being imported by Alembic
from app.models.base_class import Base  # noqa
from app.models.parts import Part # noqa
