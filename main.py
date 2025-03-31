import flet as ft
from db import database
from datetime import datetime

def main(page: ft.Page):
    page.title = 'Список дел'
    page.padding = 40
    page.bgcolor = ft.Colors.GREY_600
    page.theme_mode = ft.ThemeMode.DARK

    tasks_container = ft.Column(spacing=10)
    sort_by_creation_date = True
    sort_by_completion_status = False
    filter_in_progress = False

    def refresh_task_list():
        tasks_container.controls.clear()
        tasks = database.fetch_tasks(sort_by_creation_date, sort_by_completion_status, filter_in_progress)
        for task_id, description, date_added, task_status in tasks:
            tasks_container.controls.append(render_task(task_id, description, date_added, task_status))
        page.update()

    def render_task(task_id, description, date_added, task_status):
        task_textbox = ft.TextField(value=description, expand=True, dense=True, read_only=True)
        status_icon = (
            ft.Icons.CHECK_CIRCLE if task_status == 1 else 
            ft.Icons.RADIO_BUTTON_UNCHECKED if task_status == 0 else 
            ft.Icons.HOURGLASS_EMPTY
        )

        def toggle_task_status(e):
            new_status = (task_status + 1) % 3
            database.update_task_status(task_id, new_status)
            refresh_task_list()

        def enable_task_edit(e):
            task_textbox.read_only = False
            page.update()

        def save_task_edit(e):
            database.modify_task(task_id, task_textbox.value)
            task_textbox.read_only = True
            page.update()

        return ft.Row([
            ft.IconButton(icon=status_icon, icon_color=ft.Colors.GREEN_400 if task_status == 1 else ft.Colors.GREY_400, on_click=toggle_task_status),
            ft.Text(f"📅 {date_added}", size=12, color=ft.Colors.GREY_300),
            task_textbox,
            ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.YELLOW_400, on_click=enable_task_edit),
            ft.IconButton(icon=ft.Icons.SAVE, icon_color=ft.Colors.GREEN_400, on_click=save_task_edit)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_new_task(e):
        if task_input.value.strip():
            database.insert_task(task_input.value)
            task_input.value = ""
            refresh_task_list()

    def toggle_date_sorting(e):
        nonlocal sort_by_creation_date
        sort_by_creation_date = not sort_by_creation_date
        refresh_task_list()

    def toggle_status_sorting(e):
        nonlocal sort_by_completion_status
        sort_by_completion_status = not sort_by_completion_status
        refresh_task_list()

    def remove_completed_tasks(e):
        database.clear_completed_tasks()
        refresh_task_list()

    def filter_tasks_in_progress(e):
        nonlocal filter_in_progress
        filter_in_progress = not filter_in_progress
        refresh_task_list()

    task_input = ft.TextField(hint_text='Введите новую задачу', expand=True, dense=True, max_length=100)
    add_task_button = ft.ElevatedButton("Добавить", on_click=add_new_task, icon=ft.Icons.ADD)
    sort_by_date_button = ft.ElevatedButton("📅 Сортировать по дате", on_click=toggle_date_sorting)
    sort_by_status_button = ft.ElevatedButton("✅ Сортировать по статусу", on_click=toggle_status_sorting)
    delete_completed_button = ft.ElevatedButton("Удалить выполненные", on_click=remove_completed_tasks)
    show_in_progress_button = ft.ElevatedButton("В работе", on_click=filter_tasks_in_progress)

    page.add(
        ft.Column([
            ft.Row([task_input, add_task_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([sort_by_date_button, sort_by_status_button, show_in_progress_button], alignment=ft.MainAxisAlignment.CENTER),
            delete_completed_button,
            tasks_container
        ])
    )

    refresh_task_list()

if __name__ == '__main__':
    database.initialize_db()
    ft.app(target=main)
