import datetime
from enum import Enum

from pydantic import BaseModel, Field


# from database import ConfigurationOrm


class TypesOfDevices(Enum):
    cisco_ios = "cisco_ios"
    eltex = "eltex"
    mikrotik_routeros = 'mikrotik_routeros'
    no = 'no'


class Authdata(BaseModel):
    device_type: TypesOfDevices = "cisco_ios"
    device_name: str
    device_ip: str
    username: str
    password: str


class Configuration(BaseModel):
    id: int = 0
    device_type: TypesOfDevices = "no"
    device_name: str = "не найдено в БД"
    device_ip: str = "не найден в БД"
    config: str = "Конфигурации для данного устройства не найдено в БД"
    # created_at: datetime.datetime
    created_at: str = "не сохранялась в БД"

    # def to_conf(self, orm):
    #     self.device_type = orm.device_type
    #     self.device_name = orm.device_name
    #     self.device_ip = orm.device_ip
    #     self.config = orm.config
    #     self.created_at = orm.created_at.strftime('%d %B %Y %H:%M')
    #     return self

class FilterForm(BaseModel):
    ip_addr: str = Field(json_schema_extra={'search_url': '/api/forms/search_ip', 'placeholder': 'Фильтр по IP...'})

class FilterForm2(BaseModel):
    name: str = Field(json_schema_extra={'search_url': '/api/forms/search_name', 'placeholder': 'Фильтр по имени устройства...'})