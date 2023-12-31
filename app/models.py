import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON, TIMESTAMP, ForeignKey, Boolean

metadata = MetaData()

# role = Table('role', metadata,
#              Column('id', Integer, primary_key=True),
#              Column('name', String, nullable=False),
#              Column('permissions', JSON))

user = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('email', String, nullable=False),
             Column('username', String, nullable=False),
             Column('hashed_password', String, nullable=False),
             Column('registered_at', TIMESTAMP, default=datetime.datetime.utcnow()),
             Column('is_active', Boolean, default=True, nullable=False),
             Column('is_superuser', Boolean, default=True, nullable=False),
             Column('is_verified', Boolean, default=True, nullable=False))