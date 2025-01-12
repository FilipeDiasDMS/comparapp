import flet as ft


def main(page: ft.Page):
    page.title = 'Comparador de preços'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_min_width = 350
    page.window_min_height = 300

    # Funções para calcular e comparar os valores
    def calcular1():
        try:
            price = float(pr1.value)
            peso = float(ps1.value)
            return price / peso
        except ValueError:
            return None

    def calcular2():
        try:
            price = float(pr2.value)
            peso = float(ps2.value)
            return price / peso
        except ValueError:
            return None

    def compara():
        resultado1 = calcular1()
        resultado2 = calcular2()

        # Atualiza os textos dos resultados
        if resultado1 is not None:
            result_1.value = f"{resultado1:.3f} R$/g"
        else:
            result_1.value = "Valor inválido"

        if resultado2 is not None:
            result_2.value = f"{resultado2:.3f} R$/g"
        else:
            result_2.value = "Valor inválido"

        # Atualiza a comparação final
        if resultado1 is not None and resultado2 is not None:
            if resultado1 < resultado2:
                display_final.value = "O produto 1 está mais barato"
            elif resultado1 > resultado2:
                display_final.value = "O produto 2 está mais barato"
            else:
                display_final.value = "Os produtos têm o mesmo preço por grama"
        else:
            display_final.value = "Insira informações válidas"

        # Atualiza os textos na interface
        page.update()

    # Componentes da interface
    title = ft.Text(value='COMPARE E PAGUE MENOS', text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)

    pr1 = ft.TextField(label="Preço (R$) do produto 1", on_change=lambda e: compara())
    ps1 = ft.TextField(label="Peso (g) do produto 1", on_change=lambda e: compara())
    pr2 = ft.TextField(label="Preço (R$) do produto 2", on_change=lambda e: compara())
    ps2 = ft.TextField(label="Peso (g) do produto 2", on_change=lambda e: compara())

    result_1 = ft.Text(value="Resultado 1: ")
    result_2 = ft.Text(value="Resultado 2: ")
    display_final = ft.Text(value="Resultado Final: ")

    # Adiciona os componentes à página
    page.add(
        title,
        pr1,
        ps1,
        pr2,
        ps2,
        ft.Divider(),
        result_1,
        result_2,
        display_final,
    )


# Inicializa o aplicativo
ft.app(target=main)
