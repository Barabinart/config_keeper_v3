from fastapi import APIRouter, Request

from fastui.forms import SelectSearchResponse
from func_config import save_configuration, get_last_configuration, get_all_configurations, \
    get_all_filtr_ip_configurations, get_list_ip, get_list_name, get_all_filtr_name_configurations, \
    get_one_configuration
from schemas import Authdata, FilterForm, FilterForm2
from fastapi.responses import Response
from fastui import FastUI, AnyComponent, components as c
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent
from dotenv import load_dotenv
import os
from shared import demo_page, tabs

load_dotenv()
serv_url = os.getenv("SERVER_URL")

config_router = APIRouter(
    prefix="/config",
    tags=["Работа с конфигурациями"],
)

view_config_router = APIRouter(
    prefix="/api/fastui/config",
    tags=["FAST UI методы конфигураций"],
)

view_forms_router = APIRouter(
    prefix="/api/forms",
    tags=["FAST UI методы форм"],
)


# def config_save(auth: Annotated[Authdata, Depends()], ):
@config_router.post("/save")
def config_save(auth: Authdata):
    rezult = Response(content=save_configuration(auth), media_type="text/plain")
    return rezult


@config_router.get("/get_last")
def config_get_last(device_ip: str):
    last = get_last_configuration(device_ip)
    last_config = Response(content=last.config, media_type="text/plain")
    return last_config


@view_config_router.get("/view_all/", response_model=FastUI, response_model_exclude_none=True)
def view_all_http(page: int = 1) -> list[AnyComponent]:
    page_size = 10
    table_configs = get_all_configurations()
    return demo_page(
        *tabs(),
        c.Heading(text="Все конфигурации:", level=3),  # renders `<h2>Users</h2>`
        c.Table(
            data=table_configs[(page - 1) * page_size: page * page_size],
            columns=[
                DisplayLookup(field='id', title="ID:", on_click=GoToEvent(
                    url=serv_url + '/fastui/config/get_one/{id}/'), table_width_percent=10),
                DisplayLookup(field='device_ip', title="IP адрес:", table_width_percent=20),
                DisplayLookup(field='device_name', title="Имя устройства:", table_width_percent=20),
                DisplayLookup(field='device_type', title="Тип устройства:", table_width_percent=25),
                DisplayLookup(field='created_at', title="Время сохранения(UTC):", table_width_percent=25),
                ],
            ),
        c.Pagination(page=page, page_size=page_size, total=len(table_configs)),
        # title='Все конфигурации:',
        )


@view_config_router.get("/view_all/filtr_by_ip", response_model=FastUI, response_model_exclude_none=True)
def view_all_http(page: int = 1, ip_addr: str | None = None) -> list[AnyComponent]:
    if ip_addr:
        table_configs = get_all_filtr_ip_configurations(ip_addr)
        # print(f"я попал в {page}")
    else:
        table_configs = get_all_configurations()
        # print("я попал в 2")
    filter_form_initial = {}
    page_size = 10
    return demo_page(
        *tabs(),
        c.ModelForm(
            model=FilterForm,
            submit_url='.',
            initial=filter_form_initial,
            method='GOTO',
            submit_on_change=True,
            display_mode='inline',
        ),
        c.Heading(text="Все конфигурации:", level=3),  # renders `<h2>Users</h2>`
        c.Table(
            data=table_configs[(page - 1) * page_size: page * page_size],
            columns=[
                DisplayLookup(field='id', title="ID:", on_click=GoToEvent(
                    url=serv_url + '/fastui/config/get_one/{id}/'), table_width_percent=10),
                DisplayLookup(field='device_ip', title="IP адрес:", table_width_percent=20),
                DisplayLookup(field='device_name', title="Имя устройства:", table_width_percent=20),
                DisplayLookup(field='device_type', title="Тип устройства:", table_width_percent=25),
                DisplayLookup(field='created_at', title="Время сохранения(UTC):", table_width_percent=25),
                ],
            ),
        c.Pagination(page=page, page_size=page_size, total=len(table_configs)),
        # title='Все конфигурации:',
        )


@view_config_router.get("/view_all/filtr_by_name", response_model=FastUI, response_model_exclude_none=True)
def view_all_http(page: int = 1, name: str | None = None) -> list[AnyComponent]:
    if name:
        table_configs = get_all_filtr_name_configurations(name)
        # print(f"я попал в {page}")
    else:
        table_configs = get_all_configurations()
        # print("я попал в 2")
    filter_form_initial = {}
    page_size = 10
    return demo_page(
        *tabs(),
        c.ModelForm(
            model=FilterForm2,
            submit_url='.',
            initial=filter_form_initial,
            method='GOTO',
            submit_on_change=True,
            display_mode='inline',
        ),
        c.Heading(text="Все конфигурации:", level=3),  # renders `<h2>Users</h2>`
        c.Table(
            data=table_configs[(page - 1) * page_size: page * page_size],
            columns=[
                DisplayLookup(field='id', title="ID:", on_click=GoToEvent(
                    url=serv_url + '/fastui/config/get_one/{id}/'), table_width_percent=10),
                DisplayLookup(field='device_ip', title="IP адрес:", table_width_percent=20),
                DisplayLookup(field='device_name', title="Имя устройства:", table_width_percent=20),
                DisplayLookup(field='device_type', title="Тип устройства:", table_width_percent=25),
                DisplayLookup(field='created_at', title="Время сохранения(UTC):", table_width_percent=25),
                ],
            ),
        c.Pagination(page=page, page_size=page_size, total=len(table_configs)),
        # title='Все конфигурации:',
        )


@view_config_router.get("/get_last_one/{device_ip}/", response_model=FastUI, response_model_exclude_none=True)
def get_last_one_http(device_ip: str) -> list[AnyComponent]:
    last = get_last_configuration(device_ip)
    if last.device_ip == "не найден в БД":
        last_device_type = "не найден в БД"
    else:
        last_device_type = last.device_type.value
    return demo_page(
        c.Heading(text=f"IP: {last.device_ip}", level=4),
        c.Heading(text=f"Устройство: {last.device_name}", level=5),
        c.Heading(text=f"Производитель: {last_device_type}", level=5),
        c.Heading(text=f"Время сохранения в БД (UTC): {last.created_at}", level=5),
        c.Code(
            # language='python',
            text=last.config,
            ),
        )

@view_config_router.get("/get_one/{id}/", response_model=FastUI, response_model_exclude_none=True)
def get_one_http(id: int) -> list[AnyComponent]:
    one = get_one_configuration(id)
    if one.id == 0:
        one_device_type = "не найден в БД"
    else:
        one_device_type = one.device_type.value
    return demo_page(
        c.Heading(text=f"IP: {one.device_ip}", level=4),
        c.Heading(text=f"Устройство: {one.device_name}", level=5),
        c.Heading(text=f"Производитель: {one_device_type}", level=5),
        c.Heading(text=f"Время сохранения в БД (UTC): {one.created_at}", level=5),
        c.Code(
            # language='python',
            text=one.config,
            ),
        )

@view_forms_router.get('/search_ip', response_model=SelectSearchResponse)
async def search_view(request: Request, q: str) -> SelectSearchResponse:
    list_ip = get_list_ip(q)
    options = []
    for li in list_ip:
        options.append({'label': li, 'value': li})
    return SelectSearchResponse(options=options)


@view_forms_router.get('/search_name', response_model=SelectSearchResponse)
async def search_view(request: Request, q: str) -> SelectSearchResponse:
    list_name = get_list_name(q)
    options = []
    for li in list_name:
        options.append({'label': li, 'value': li})
    return SelectSearchResponse(options=options)
