# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db


def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in the ListView, optionally filtered by search term."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)

    for contact in contacts:
        contact_id, name, phone, email = contact
        
        # modern card for each contact
        contact_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    name,
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Edit",
                                            icon=ft.Icons.EDIT,
                                            on_click=lambda _, c=contact: open_edit_dialog(
                                                page, c, db_conn, contacts_list_view
                                            ),
                                        ),
                                        ft.PopupMenuItem(),  # Divider
                                        ft.PopupMenuItem(
                                            text="Delete",
                                            icon=ft.Icons.DELETE,
                                            on_click=lambda _, cid=contact_id: open_delete_confirmation(
                                                page, cid, db_conn, contacts_list_view
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.PHONE, size=16),
                                ft.Text(phone if phone else "No phone", size=14),
                            ],
                            spacing=8,
                        ),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.EMAIL, size=16),
                                ft.Text(email if email else "No email", size=14),
                            ],
                            spacing=8,
                        ),
                    ],
                    spacing=8,
                ),
                padding=15,
            ),
            elevation=2,
        )
        
        contacts_list_view.controls.append(contact_card)
    
    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn, search_input=None):
    """Adds a new contact with validation and refreshes the list."""
    name_input, phone_input, email_input = inputs
    
    if not name_input.value or name_input.value.strip() == "":
        name_input.error_text = "Name cannot be empty"
        page.update()
        return
    
    name_input.error_text = None
    
    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)

    for field in inputs:
        field.value = ""

    search_term = search_input.value if search_input else ""
    display_contacts(page, contacts_list_view, db_conn, search_term)
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view, search_input=None):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    
    # Get search term if search_input is provided
    search_term = search_input.value if search_input else ""
    display_contacts(page, contacts_list_view, db_conn, search_term)


def open_delete_confirmation(page, contact_id, db_conn, contacts_list_view, search_input=None):
    """Opens a confirmation dialog before deleting a contact."""
    
    def confirm_delete(e):
        delete_contact(page, contact_id, db_conn, contacts_list_view, search_input)
        dialog.open = False
        page.update()
    
    def cancel_delete(e):
        dialog.open = False
        page.update()
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("Cancel", on_click=cancel_delete),
            ft.TextButton("Yes", on_click=confirm_delete),
        ],
    )
    
    page.open(dialog)


def open_edit_dialog(page, contact, db_conn, contacts_list_view, search_input=None):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact

    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        if not edit_name.value or edit_name.value.strip() == "":
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return
        
        update_contact_db(db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value)
        dialog.open = False
        page.update()

        search_term = search_input.value if search_input else ""
        display_contacts(page, contacts_list_view, db_conn, search_term)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email], tight=True),
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=lambda e: setattr(dialog, 'open', False) or page.update(),
            ),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )

    page.open(dialog)