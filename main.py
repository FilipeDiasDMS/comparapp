import flet as ft

def main(page: ft.Page):
    page.title = "Minha Aplicação Flet"
    page.add(ft.Text("Hello, world!"))

# Iniciar o app no navegador
ft.app(target=main, view=ft.WEB_BROWSER)
