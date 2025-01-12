import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = 'Comparador de preços'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_min_width = 350
    page.window_min_height = 300

    def handle_input_change_pr_tag1(e):
        value = e.control.value
        if '.' in value and len(e.control.value.split('.')[-1]) == 2:
            ps1.focus()
        compara()

        page.update()
    def handle_input_change_ps_tag1(e):
        value = e.control.value
        if '.' in value and len(e.control.value.split('.')[-1]) == 2:
            pr2.focus()
        compara()

        page.update()

    def handle_input_change_pr_tag2(e):
        value = e.control.value
        if '.' in value and len(e.control.value.split('.')[-1]) == 2:
            ps2.focus()
        compara()

    def handle_input_change_ps_tag2(e):
        compara()

        page.update()

    divider = ft.Container(
        width=300,
        height=1,
        bgcolor='#A4A4A4',
        margin=ft.Margin (0, 0, 0, 0)
    )

    #image = ft.Image(src='https://drive.google.com/file/d/1kgEPPXIACGnAmzB0JaPRRtl19CtiEnvc/view?usp=sharing', width=300, fit=ft.ImageFit.CONTAIN)

    title = ft.Text(value='COMPARE E PAGUE MENOS', text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)

    pr_tag1 = ft.Text(value='Preço (R$) do produto 1', text_align=ft.TextAlign.LEFT, width=60, size=12)
    pr1 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_pr_tag1)

    ps_tag1 = ft.Text(value='Peso (g) do produto 1', text_align=ft.TextAlign.LEFT, width=60, size=12)
    ps1 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_ps_tag1)

    rs_tag1 = ft.Text(value='R$/g', text_align=ft.TextAlign.LEFT, width=80, size=12)

    pr_tag2 = ft.Text(value='Preço (R$) do produto 2', text_align=ft.TextAlign.LEFT, width=60, size=12)
    pr2 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_pr_tag2)

    ps_tag2 = ft.Text(value='Peso (g) do produto 2', text_align=ft.TextAlign.LEFT, width=60, size=12)
    ps2 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_ps_tag2)

    rs_tag2 = ft.Text(value='R$/g', text_align=ft.TextAlign.LEFT, width=80, size=12)

    result_1 = ft.Text(value='Resultado 1', size=12)
    result_2 = ft.Text(value='Resultado 2', size=12)
    display_final = ft.Text(value='Resultado Final', size=12)



    def calcular1():
        try:
            price = float(pr1.value)  # Usando pr1.value em vez de pr1.get()
            peso = float(ps1.value)   # Usando ps2.value em vez de ps1.get()
            resultado1 = price / peso
            result_1.value = f'{resultado1:.3f}'
            result_1.update()  # Atualiza o texto de result_1
            return resultado1
        except ValueError:
            result_1.value = "Valor inválido"
            result_1.update()
            return 0

    def calcular2():
        try:
            price2 = float(pr2.value)  # Usando pr1.value
            peso2 = float(ps2.value)   # Usando ps2.value
            resultado2 = price2 / peso2
            result_2.value = f'{resultado2:.3f}'
            result_2.update()  # Atualiza o texto de result_2
            return resultado2
        except ValueError:
            result_2.value = "Valor inválido"
            result_2.update()
            return 0

    def compara():

        if not pr1.value or not ps1.value or pr1.value == '' or ps1.value == '':
            display_final.value = 'Insira informações válidas'
        elif not pr2.value or not ps2.value or pr2.value =='' or ps2.value == '':
            display_final.value = 'Insira informações válidas'

        else:
            resultado1 = calcular1()
            resultado2 = calcular2()
            if resultado2 > resultado1:
                display_final.value = f'O produto 2 está mais caro'
            elif resultado2 == resultado1:
                display_final.value = f'Ambo custam o mesmo'
            else:
                display_final.value = f'O produto 1 está mais caro'

        display_final.update()  # Atualiza o texto de display_final

    def auto_update():

        page.add(
            ft.Row([title],alignment=ft.MainAxisAlignment.CENTER ),
            ft.Row([pr_tag1, pr1, ps_tag1, ps1], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([pr_tag2, pr2, ps_tag2, ps2],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([rs_tag1, result_1, rs_tag2, result_2], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([divider],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([display_final], alignment=ft.MainAxisAlignment.CENTER),
        )

    auto_update()

# Inicializa o aplicativo
ft.app(target=main)
