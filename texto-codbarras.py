# 100SECURITY
# Converter Texto <> Código de Barras
# Por: Marcos Henrique
# Site: www.100security.com.br

import os
import re
import unicodedata
from colorama import Fore, Style
from barcode.codex import Code128
from barcode.writer import ImageWriter
from pyzbar.pyzbar import decode
from PIL import Image

# Limpar a Tela
def clear_screen():
    if os.name == 'nt':  # Se for Windows
        os.system('cls')
    else:  # Se for Linux ou macOS
        os.system('clear')

clear_screen()

# Inicializa o Colorama
from colorama import init
init(autoreset=True)

# Banner
projeto = f"{Style.BRIGHT}{Fore.YELLOW}# - - - - - - - - 100SECURITY - - - - - - - - #\n"
titulo = f"{Style.BRIGHT}{Fore.GREEN}Converter Texto <> Código de Barras"
github = f"{Style.BRIGHT}{Fore.WHITE}GitHub: {Fore.WHITE}github.com/100security/{Style.BRIGHT}{Fore.LIGHTCYAN_EX}texto-codbarras"
instagram = f"{Style.BRIGHT}{Fore.WHITE}Instagram: {Fore.WHITE}{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}@100security"

# Exibe o texto com as cores e com uma nova linha entre eles
print(f"{projeto}\n{titulo}\n{github}\n{instagram}")

# Função para remover acentos e caracteres não suportados
def remover_acentos_e_caracteres_especiais(text):
    # Normaliza o texto para remover acentos
    normalized_text = unicodedata.normalize('NFKD', text)
    # Remove os caracteres não ASCII (acentuações) e caracteres especiais, deixando apenas letras e números
    text_sem_acentos = re.sub(r'[^\w\s]', '', normalized_text)
    # Substitui espaços por underline para preservá-los no código de barras
    text_substituido = text_sem_acentos.replace(' ', '_')
    return text_substituido

# Função para salvar código de barras em PNG
def gerar_codigo_de_barras(text, output_image):
    try:
        # Remover acentos e caracteres não suportados
        text_limpo = remover_acentos_e_caracteres_especiais(text)
        if not text_limpo:
            raise ValueError("O texto inserido não contém caracteres válidos para Code 128.")

        # Criar o código de barras no formato Code128 sem texto legível
        writer = ImageWriter()
        writer.text = ''  # Remove o texto legível do código de barras
        writer_options = {'write_text': False}  # Configuração para não escrever o texto
        
        # Gera o código de barras com o texto limpo
        codigo_de_barras = Code128(text_limpo, writer=writer)
        codigo_de_barras.save(output_image, options=writer_options)
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Código de barras salvo como {output_image}.png")
    
    except ValueError as ve:
        print(f"{Style.BRIGHT}{Fore.RED}Erro: {ve}")
    
    except Exception as e:
        print(f"{Style.BRIGHT}{Fore.RED}Erro ao gerar código de barras: {e}")

# Função para ler código de barras de uma imagem
def ler_codigo_de_barras(image_path):
    try:
        img = Image.open(image_path)
        decoded_objects = decode(img)
        if decoded_objects:
            for obj in decoded_objects:
                # Decodifica o texto e substitui os underlines por espaços
                decoded_text = obj.data.decode('utf-8').replace('_', ' ')
                print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Código de Barras detectado: {decoded_text}")
                # Salva o texto decodificado em um arquivo
                salvar_em_arquivo('codbarras.txt', decoded_text)
        else:
            print(f"{Style.BRIGHT}{Fore.RED}Nenhum código de barras detectado na imagem.")
    except Exception as e:
        print(f"{Style.BRIGHT}{Fore.RED}Erro ao ler código de barras: {e}")

# Função para salvar o conteúdo em um arquivo
def salvar_em_arquivo(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}Resultado salvo em {file_name}")

# Função para exibir o menu
def exibir_menu():
    print(f"\n{Style.BRIGHT}{Fore.RED}# - - - - - - - - - M E N U - - - - - - - - - #\n")
    print(f"{Style.BRIGHT}{Fore.WHITE}1 {Style.NORMAL}{Fore.WHITE}- Converter {Style.BRIGHT}{Fore.LIGHTCYAN_EX}Texto {Fore.WHITE}para {Style.BRIGHT}{Fore.LIGHTYELLOW_EX}Código de Barras")
    print(f"{Style.BRIGHT}{Fore.WHITE}2 {Style.NORMAL}{Fore.WHITE}- Ler {Style.BRIGHT}{Fore.LIGHTYELLOW_EX}Código de Barras {Fore.WHITE}de {Style.BRIGHT}{Fore.LIGHTCYAN_EX}Imagem")
    print(f"{Style.BRIGHT}{Fore.WHITE}3 {Style.NORMAL}{Fore.WHITE}- {Style.BRIGHT}{Fore.LIGHTRED_EX}Sair\n")

# Função principal
def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            texto = input("Digite o Texto a ser convertido para Código de Barras: ")
            output_image = 'codigo_de_barras'  # A extensão .png será adicionada automaticamente
            gerar_codigo_de_barras(texto, output_image)
        
        elif opcao == '2':
            image_path = input("Digite o nome da imagem com o Código de Barras (ex: codbarras.png): ")
            ler_codigo_de_barras(image_path)
        
        elif opcao == '3':
            print(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}Saindo...")
            break

        else:
            print(f"{Style.BRIGHT}{Fore.RED}Opção inválida. Tente novamente.")

# Executar o programa
if __name__ == "__main__":
    main()
