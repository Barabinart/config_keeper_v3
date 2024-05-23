from netmiko import ConnectHandler
from sqlalchemy import distinct
from database import new_session, ConfigurationOrm
from schemas import Authdata, Configuration
import difflib

# метод для сохранения конфигурации
def save_configuration(auth: Authdata):
    # создаем элемент в котором содержится необходимая информация для авторизации на устройстве
    device = {
        "device_type": auth.device_type.value,
        "host": auth.device_ip,
        "username": auth.username,
        "password": auth.password,
    }
    try:
        ssh_session = ConnectHandler(**device)
        if auth.device_type.value != "mikrotik_routeros":
            configuration = ssh_session.send_command("show running-config")
        else:
            configuration = ssh_session.send_command("export compact")
            # удаление времени снятия конфигурации у оборудования Mikrotik
            lines = configuration.split('by')
            lines = lines[1:]
            configuration = '#'+'by'.join(lines)
        ssh_session.disconnect()
    except Exception as e:
        # raise HTTPException(status_code=400, detail=f"Ошибка подключения к устройству: {str(e)}")
        return f"Ошибка подключения к устройству: {str(e)}"
    with new_session() as session:
        last_config = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_ip == auth.device_ip).order_by(
            ConfigurationOrm.created_at.desc()).first()

        if last_config and last_config.config == configuration:
            return "Конфигурация идентична последней, сохранение не требуется"
        new_config = ConfigurationOrm(
            device_type=auth.device_type.value,
            device_ip=auth.device_ip,
            device_name=auth.device_name,
            config=configuration,
        )
        session.add(new_config)
        session.commit()
    return "Конфигурация успешно сохранена"


# Метод для просмотра последней конфигурации
def get_last_configuration(device_ip):
    with new_session() as session:
        last_config_orm = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_ip == device_ip).order_by(
            ConfigurationOrm.created_at.desc()).first()
        if last_config_orm:
            last_config = Configuration(
                id=last_config_orm.id,
                device_type=last_config_orm.device_type.value,
                device_name=last_config_orm.device_name,
                device_ip=last_config_orm.device_ip,
                config=last_config_orm.config,
                created_at=last_config_orm.created_at.strftime('%d %B %Y %H:%M'),
            )
            return last_config
        else:
            return Configuration()


def get_one_configuration(device_id):
    with new_session() as session:
        one_config_orm = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.id == device_id).first()
        if one_config_orm:
            one_config = Configuration(
                id=one_config_orm.id,
                device_type=one_config_orm.device_type.value,
                device_name=one_config_orm.device_name,
                device_ip=one_config_orm.device_ip,
                config=one_config_orm.config,
                created_at=one_config_orm.created_at.strftime('%d %B %Y %H:%M'),
            )
            return one_config
        else:
            return Configuration()


# возвращает различая конфигураций: парвая- соответствует полученному ID и предыдущая этого же устройства
def get_diff(device_id):
    with new_session() as session:
        first_config_orm = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.id == device_id).first()
        if first_config_orm:
            first_config = first_config_orm.config
            # print(first_config_orm.id)
            configurations_orm = session.query(ConfigurationOrm).filter(
                ConfigurationOrm.device_ip == first_config_orm.device_ip).order_by(
                ConfigurationOrm.id.desc()).all()

            for config_orm in configurations_orm:
                if config_orm.id < device_id:
                    two_config = config_orm.config
                    # print(config_orm.id)
                    d = difflib.Differ()
                    diff = list(d.compare(two_config.splitlines(), first_config.splitlines()))
                    return diff
            return ["* В БД нет предыдущей конфигурации для этого устройства."]
        else:
            return ["* Конфигурация не найдена."]


# возвращает различая конфигураций: первая - соответствует последней по полученному IP и предыдущая этого же устройства
def get_diff_last(device_ip):
    with new_session() as session:
        first_config_orm = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_ip == device_ip).order_by(
            ConfigurationOrm.created_at.desc()).first()
        if first_config_orm:
            first_config = first_config_orm.config
            # print(first_config_orm.id)
            two_config_orm = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_ip == device_ip).order_by(
            ConfigurationOrm.created_at.desc()).offset(1).first()
            if two_config_orm:
                two_config = two_config_orm.config
                # print(two_config_orm.id)
                d = difflib.Differ()
                diff = list(d.compare(two_config.splitlines(), first_config.splitlines()))
                return diff
            return ["* В БД нет предыдущей конфигурации для этого устройства."]
        else:
            return ["* Конфигурация не найдена."]


# Метод выдачи списка всех конфигураций
def get_all_configurations():
    with new_session() as session:
        configurations_orm = session.query(ConfigurationOrm).order_by(
            ConfigurationOrm.created_at.desc()).all()
        configurations = []
        if not configurations_orm:
            config = Configuration()
            configurations.append(config)
        else:
            for config_orm in configurations_orm:
                config = Configuration(
                    id=config_orm.id,
                    device_type=config_orm.device_type.value,
                    device_name=config_orm.device_name,
                    device_ip=config_orm.device_ip,
                    config=config_orm.config,
                    created_at=config_orm.created_at.strftime('%d %B %Y %H:%M'),
                    )
                configurations.append(config)
        return configurations


# Метод выдачи списка всех конфигураций фильтр по IP, сортировка по дате
def get_all_filtr_ip_configurations(device_ip):
    with new_session() as session:
        configurations_orm = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_ip == device_ip).order_by(
            ConfigurationOrm.created_at.desc()).all()
        configurations = []
        if not configurations_orm:
            config = Configuration()
            configurations.append(config)
        else:
            for config_orm in configurations_orm:
                config = Configuration(
                    id=config_orm.id,
                    device_type=config_orm.device_type.value,
                    device_name=config_orm.device_name,
                    device_ip=config_orm.device_ip,
                    config=config_orm.config,
                    created_at=config_orm.created_at.strftime('%d %B %Y %H:%M'),
                    )
                configurations.append(config)
        return configurations


# Метод выдачи списка всех IP для строки поиска
def get_list_ip(q: str):
    with new_session() as session:
        list_unik_ip = session.query(distinct(ConfigurationOrm.device_ip)).all()
    new_list = []
    for i in list_unik_ip:
        if q in i[0]:
            new_list.append(i[0])
    return new_list


# Метод выдачи списка всех конфигураций фильтр по имени, сортировка по дате
def get_all_filtr_name_configurations(name):
    with new_session() as session:
        configurations_orm = session.query(ConfigurationOrm).filter(
            ConfigurationOrm.device_name == name).order_by(
            ConfigurationOrm.created_at.desc()).all()
        configurations = []
        if not configurations_orm:
            config = Configuration()
            configurations.append(config)
        else:
            for config_orm in configurations_orm:
                config = Configuration(
                    id=config_orm.id,
                    device_type=config_orm.device_type.value,
                    device_name=config_orm.device_name,
                    device_ip=config_orm.device_ip,
                    config=config_orm.config,
                    created_at=config_orm.created_at.strftime('%d %B %Y %H:%M'),
                    )
                configurations.append(config)
        return configurations


# Метод выдачи списка всех имен устройств для строки поиска
def get_list_name(q: str):
    with new_session() as session:
        list_unik_name = session.query(distinct(ConfigurationOrm.device_name)).all()
    new_list = []
    for i in list_unik_name:
        if q in i[0]:
            new_list.append(i[0])
    return new_list
