import flet as ft
from db import main_db
from datetime import datetime


def main(page: ft.Page):
    page.title = 'Todo List'
    page.padding = 40 
    page.bgcolor = ft.Colors.GREY_600
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column(spacing=10)
    sort_by_date = True
    sort_by_status = False

    def load_tasks():
        task_list.controls.clear()
        tasks = main_db.get_tasks(sort_by_date, sort_by_status)
        for task_id, task_text, created_at, status in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, created_at, status))
        page.update()

    def create_task_row(task_id, task_text, created_at, status):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)
        status_icon = ft.Icons.CHECK_CIRCLE if status else ft.Icons.RADIO_BUTTON_UNCHECKED

        def toggle_status(e):
            new_status = not status
            main_db.update_task_status(task_id, new_status)
            load_tasks()

        def enable_edit(e):
            task_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_task_db(task_id, task_field.value)
            task_field.read_only = True
            page.update()

        return ft.Row([
            ft.IconButton(icon=status_icon, icon_color=ft.Colors.GREEN_400 if status else ft.Colors.GREY_400, on_click=toggle_status),
            ft.Text(f"📅 {created_at}", size=12, color=ft.Colors.GREY_300),
            task_field,
            ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(icon=ft.Icons.SAVE, icon_color=ft.Colors.GREEN_400, on_click=save_edit)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value.strip():
            main_db.add_task_db(task_input.value)
            task_input.value = ""
            load_tasks()

    def toggle_sort(e):
        nonlocal sort_by_date
        sort_by_date = not sort_by_date
        load_tasks()

    def toggle_sort_status(e):
        nonlocal sort_by_status
        sort_by_status = not sort_by_status
        load_tasks()

    task_input = ft.TextField(hint_text='Добавьте задачу', expand=True, dense=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD)

    sort_button = ft.ElevatedButton("📅 Сортировать по дате", on_click=toggle_sort)
    sort_status_button = ft.ElevatedButton("✅ Сортировать по статусу", on_click=toggle_sort_status)

    page.add(
        ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([sort_button, sort_status_button], alignment=ft.MainAxisAlignment.CENTER),
            task_list
        ])
    )

    load_tasks()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)
