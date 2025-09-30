# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact


def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600
    page.scroll = ft.ScrollMode.AUTO

    page.fonts = {
        "Poppins": "fonts/Poppins-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Poppins")

    def toggle_theme(e):
        if theme_switch.value:  # when switch is ON
            page.theme_mode = ft.ThemeMode.DARK
            theme_switch.label = "Light Mode"
        else:  # when switch is OFF
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_switch.label = "Dark Mode"
        page.update()

    theme_switch = ft.Switch(
        label="Dark Mode",
        value=False,  # switch off = light mode
        on_change=toggle_theme
    )

    def on_search_change(e):
        display_contacts(page, contacts_list_view, db_conn, search_input.value)
    
    search_input = ft.TextField(
        label="Search contacts by name...",
        width=350,
        prefix_icon=ft.Icons.SEARCH,
        on_change=on_search_change
    )

    db_conn = init_db()
    
    name_input = ft.TextField(label="Name", width=350)
    phone_input = ft.TextField(label="Phone", width=350)
    email_input = ft.TextField(label="Email", width=350)
    inputs = (name_input, phone_input, email_input)

    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True, padding=10)

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, search_input),
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Contact Book", size=24, weight=ft.FontWeight.BOLD),
                        theme_switch,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(),
                ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                search_input,
                contacts_list_view,
            ],
            scroll=ft.ScrollMode.AUTO,
        )
    )

    display_contacts(page, contacts_list_view, db_conn)


if __name__ == "__main__":
    ft.app(target=main)