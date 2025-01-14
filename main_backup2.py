import flet as ft
import asyncio
import cv2
import zxing
import requests
import tempfile
import threading

def main(page: ft.Page):
    page.title = 'Comparador de preços'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_min_width = 350
    page.window_min_height = 622
    page.window_max_width = 350
    page.window_max_height = 622

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

    btn_qrcode = ft.ElevatedButton (text='CÓDIGO DE BARRAS', icon=ft.icons.QR_CODE, on_click=lambda _: capture_and_decode())

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
                display_final.value = f'O produto 2 está mais caro'
            elif resultado2 == resultado1:
                display_final.value = f'Ambo custam o mesmo'
            else:
                display_final.value = f'O produto 1 está mais caro'

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
            ft.Row([desconto_container], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([btn_qrcode], alignment=ft.MainAxisAlignment.CENTER),
        )



    auto_update()

#--------------------------------------------------------------------------------------

# Inicializando o leitor ZXing
reader = zxing.BarCodeReader()

# Função para buscar informações do produto alimentar
def buscar_info_produto_alimenticio(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data.get('product'):
            produto = data['product']
            print("Informações do Produto Alimentício:")
            print(f"Nome: {produto.get('product_name', 'Desconhecido')}")
            print(f"Marca: {produto.get('brands', 'Desconhecido')}")
            print(f"Ingredientes: {produto.get('ingredients_text', 'Desconhecido')}")
            print(f"Valores nutricionais: {produto.get('nutriments', 'Desconhecido')}")
        else:
            print("Produto não encontrado.")
    else:
        print("Erro ao buscar informações.")

# Função para capturar frames em tempo real e processar com ZXing
def capture_and_decode():
    # Inicializa a captura de vídeo (webcam)
    cap = cv2.VideoCapture(0)

    def show_video():
        while True:
            # Lê o frame atual da webcam
            ret, frame = cap.read()

            if not ret:
                print("Erro ao capturar a imagem.")
                break

            # Mostra o frame em uma janela
            cv2.imshow("Video", frame)

            # Tenta salvar a imagem temporariamente para processar com ZXing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                cv2.imwrite(temp_file.name, frame)

                # Tenta detectar e decodificar o código de barras no frame
                try:
                    barcode = reader.decode(temp_file.name)
                    if barcode:
                        print(f"Tipo: {barcode.format}")
                        print(f"Dados: {barcode.raw}")

                        # Chama a função para buscar informações do produto
                        buscar_info_produto_alimenticio(barcode.raw)

                        # Desenha um retângulo em volta do código de barras
                        for rect in barcode.rect:
                            cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
                except Exception as e:
                    print(f"Erro ao processar o código de barras: {e}")

            # Espera por tecla para continuar ou sair
            key = cv2.waitKey(1)
            if key == ord('q'):  # Pressione 'q' para sair
                break

        cap.release()
        cv2.destroyAllWindows()

    video_thread = threading.Thread(target=show_video)
    video_thread.start()

# Inicializa o aplicativo
ft.app(target=main)
