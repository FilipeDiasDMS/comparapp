import flet as ft
import tempfile
import matplotlib.pyplot as plt

plt.switch_backend('Agg')

def create_plot(result_1_value, result_2_value):
    # Criando o gráfico com os valores de result_1 e result_2
    fig, ax = plt.subplots()
    fig.patch.set_facecolor ('none')
    ax.set_facecolor('none')
    ax.bar([1, 2], [result_1_value, result_2_value], tick_label=["Produto 1", "Produto 2"], color=['#bc8d27', '#976f17'], )  # Plotando os dois resultados (produto 1 e 2)
    ax.set_xticks([1, 2])  # Definindo as posições no eixo X
    ax.set_xticklabels(["Produto 1", "Produto 2"], fontsize=15, color='white')  # Nomeando os pontos do eixo X
    ax.get_yaxis().set_visible(False)
    ax.tick_params(axis='y', labelcolor='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Salvando o gráfico diretamente em um arquivo temporário
    img_path = "plot.png"
    plt.savefig(img_path, format='png')  # Salvando diretamente no caminho

    return img_path

def main(page: ft.Page):
    page.splash = None
    page.title = 'Comparador de preços'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_min_width = 350
    page.window_min_height = 680
    page.window_max_width = 350
    page.window_max_height = 700

    def reset_all_data(e):
        pr1.value = ''
        ps1.value = ''
        pr2.value = ''
        ps2.value = ''
        result_1.value = 'Resultado 1'
        result_2.value = 'Resultado 2'
        display_final.value = 'Resultado Final'
        desconto.value = 'Diferença %'
        flet_img.src = 'empty.png'
        pr1.update()
        ps1.update()
        pr2.update()
        ps2.update()
        result_1.update()
        result_2.update()
        display_final.update()
        desconto.update()
        flet_img.update()

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

    def update_plot(result_1_value, result_2_value):
        img_path = create_plot(result_1_value, result_2_value)

        # Atualizando o caminho da imagem no Flet
        flet_img.src = img_path
        flet_img.update()

    global flet_img
    flet_img = ft.Image(src='empty.png', width=300, height=200)

    plot = ft.Container(
        content=flet_img,
        width=302,
        height=202,
        margin=ft.Margin(0, 0, 0, 0))

    #btn_plot = ft.ElevatedButton(text="Gerar Gráfico", on_click=lambda _: asyncio.run(update_plot(calcular1(), calcular2())))

    title = ft.Text(value='COMPARE E PAGUE MENOS', text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)

    pr_tag1 = ft.Text(value='Preço (R$) do produto 1', text_align=ft.TextAlign.LEFT, width=60, size=12)
    pr1 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_pr_tag1)

    ps_tag1 = ft.Text(value='Peso (g) do produto 1', text_align=ft.TextAlign.LEFT, width=60, size=12)
    ps1 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_ps_tag1)

    rs_tag1 = ft.Text(value='R$/g', text_align=ft.TextAlign.LEFT, width=70, size=12)

    pr_tag2 = ft.Text(value='Preço (R$) do produto 2', text_align=ft.TextAlign.LEFT, width=60, size=12)
    pr2 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_pr_tag2)

    ps_tag2 = ft.Text(value='Peso (g) do produto 2', text_align=ft.TextAlign.LEFT, width=60, size=12)
    ps2 = ft.TextField(text_align=ft.TextAlign.LEFT, text_size=12, width=80, height=40, bgcolor='light blue', on_change=handle_input_change_ps_tag2)

    rs_tag2 = ft.Text(value='R$/g', text_align=ft.TextAlign.LEFT, width=70, size=12)

    result_1 = ft.Text(value='Resultado 1', size=12)
    result_2 = ft.Text(value='Resultado 2', size=12)
    display_final = ft.Text(value='Resultado Final', size=12)

    desconto = ft.Text(value='Diferença %', size=12, width=160, text_align=ft.TextAlign.CENTER)

    btn_reset = ft.ElevatedButton(icon=ft.icons.RESTART_ALT, text="Reiniciar",bgcolor='#bc8d27',color='white', on_click=reset_all_data)

    desconto_container = ft.Container(content=desconto,
        width=200,
        height=20,
        bgcolor='#bc8d27',
        margin=ft.Margin(0, 0, 0, 0),
        border_radius=5)

    title = ft.Container(content=title,
        width=300,
        height=60,
        bgcolor='#bc8d27',
        margin=ft.Margin(0, -20, 0, 10),
        border_radius=15,
        alignment=ft.alignment.bottom_center,
        padding=10)

    btn_qrcode = ft.FloatingActionButton (icon=ft.icons.QR_CODE, on_click=lambda _: capture_and_decode())

    row_withbg = ft.Container(
        content=ft.Row([rs_tag1, result_1, rs_tag2, result_2],
        alignment=ft.MainAxisAlignment.CENTER),
        bgcolor = '#bc8d27',
        padding = 10,
    )

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
                display_final.value = f'O produto 1 está mais barato'
            elif resultado2 == resultado1:
                display_final.value = f'Ambo custam o mesmo'
            else:
                display_final.value = f'O produto 2 está mais barato'
            update_plot(resultado1, resultado2)

        display_final.update()  # Atualiza o texto de display_final

        try:
            dif1 = float(result_1.value)
            dif2 = float(result_2.value)
            dif =  dif1 - dif2
            dif_porc = dif * 1000
            desconto.value = f'A diferença é de {abs(dif_porc):.2f}%'
            desconto.update()
        except ValueError:
            desconto.value = 'Valores inválidos'
            desconto.update()

    def auto_update():

        page.add(
            ft.Row([title],alignment=ft.MainAxisAlignment.CENTER ),
            ft.Row([pr_tag1, pr1, ps_tag1, ps1], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([pr_tag2, pr2, ps_tag2, ps2],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([row_withbg], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([divider],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([display_final], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([btn_reset], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([plot], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([desconto_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([btn_qrcode], alignment=ft.MainAxisAlignment.END),
        )

    auto_update()
# Inicializa o aplicativo
ft.app(target=main)
