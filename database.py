import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from schemas import TypesOfDevices

# создаем движок базы данных
engine = create_engine(
    "sqlite:///./db/configurations.db"
)

# создаем сессию к бд
new_session = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


# создаем таблицу
class ConfigurationOrm(Base):
    __tablename__ = "Configurations"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_type: Mapped[TypesOfDevices] = mapped_column()
    # device_type: Mapped[str] = mapped_column()
    device_name: Mapped[str] = mapped_column()
    device_ip: Mapped[str] = mapped_column()
    config: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    # created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc',now())"))


# создаем таблице в БД
def create_tables():
    Base.metadata.create_all(engine)
    # engine.echo = True
