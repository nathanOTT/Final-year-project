from __future__ import with_statement
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import your project's models
from database.config import Base  # Import the Base metadata
from database import models  # Import the models themselves to be registered with Alembic

# This is the Alembic Config object, which provides access to the .ini file
config = context.config

# Setting target_metadata to the Base.metadata object from your models
target_metadata = Base.metadata  # This line tells Alembic which metadata to use

# Other Alembic setup remains the same
fileConfig(config.config_file_name)
