from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent
from dotenv import load_dotenv
import os

load_dotenv()
serv_url = os.getenv("SERVER_URL")
zab_url = os.getenv("ZABBIX_URL")

def demo_page(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"ConfigKeeper — {title}" if title else "ConfigKeeper"),
        c.Navbar(
            title="ConfigKeeper",
            title_event=GoToEvent(url=serv_url + "/fastui/config/view_all/"),
            start_links=[
                c.Link(
                    components=[c.Text(text="Все конфигурации")],
                    on_click=GoToEvent(url=serv_url + "/fastui/config/view_all/"),
                    # active="startswith:" + "/fastui/config/view_all/",
                ),
                c.Link(
                    components=[c.Text(text="СУМ КС")],
                    on_click=GoToEvent(url=zab_url),
                    # active="startswith:" + "/fastui/config/view_all/",
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text='ConfigKeeper by BarabinArt 2024',
            links=[
                c.Link(
                    components=[c.Text(text="ConfigKeeper")], on_click=GoToEvent(
                        url=serv_url + "/fastui/config/view_all/")
                ),
                c.Link(components=[c.Text(text='СУМ КС')], on_click=GoToEvent(url=zab_url)),
            ],
        ),
    ]

def tabs() -> list[AnyComponent]:
    return [
        c.LinkList(
            links=[
                c.Link(
                    components=[c.Text(text='Фильтр по IP')],
                    on_click=GoToEvent(url=serv_url + "/fastui/config/view_all/filtr_by_ip"),
                    active='startswith:/fastui/config/view_all/filtr_by_ip',
                ),
                c.Link(
                    components=[c.Text(text='Фильтр по имени устройства')],
                    on_click=GoToEvent(url=serv_url + "/fastui/config/view_all/filtr_by_name"),
                    active='startswith:/fastui/config/view_all/filtr_by_name',
                ),
            ],
            mode='tabs',
            class_name='+ mb-4',
        ),
    ]