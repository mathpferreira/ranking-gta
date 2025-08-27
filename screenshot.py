from PIL import Image, ImageDraw, ImageFont
import requests
import os
from datetime import datetime

def main():
    # URL do CSV do Google Sheets
    url = "https://docs.google.com/spreadsheets/d/1DS24AMuYnkEJTDVaNHeAB1gGEoz6YOew4IckQD7JjOw/export?format=csv&gid=0"
    response = requests.get(url)
    response.encoding = "utf-8"
    linhas = response.text.splitlines()

    # Top 3 (ignora cabeçalho)
    top3 = [linha.split(",") for linha in linhas[1:4]]

    # Criar imagem
    largura, altura = 600, 400
    img = Image.new("RGB", (largura, altura), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype("arialbd.ttf", 72)  # Título bem grande
        font_texto = ImageFont.truetype("arialbd.ttf", 54)   # Jogadores maiores
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # --- Título ---
    titulo = "HALL DA FAMA"
    bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
    w = bbox[2] - bbox[0]
    x_titulo = (largura - w) / 2
    y_titulo = 40

    # Glow RGB (3 sombras: vermelho, verde, azul)
    for dx, dy, cor in [(3, 0, (255, 0, 0)), (-3, 0, (0, 255, 0)), (0, 3, (0, 128, 255))]:
        draw.text((x_titulo + dx, y_titulo + dy), titulo, font=font_titulo, fill=cor)

    # Texto principal (branco forte)
    draw.text((x_titulo, y_titulo), titulo, font=font_titulo, fill=(255, 255, 255))

    # --- Jogadores ---
    y = 160
    cores = [(218, 165, 32), (215, 215, 215), (176, 141, 87)]  # ouro, prata, bronze
    for i, jogador in enumerate(top3):
        if len(jogador) < 2:
            continue
        nome, pontos = jogador[0], jogador[1]
        texto = f"{nome} - {pontos} pontos"

        # Centralizar
        bbox = draw.textbbox((0, 0), texto, font=font_texto)
        w = bbox[2] - bbox[0]
        x = (largura - w) / 2

        # Glow (sombra preta leve pra destacar)
        draw.text((x + 2, y + 2), texto, font=font_texto, fill=(0, 0, 0))
        # Texto principal colorido
        draw.text((x, y), texto, font=font_texto, fill=cores[i])

        y += 65  # espaçamento menor

    # Salvar imagem dentro de docs/
    os.makedirs("docs", exist_ok=True)
    output_path = os.path.join("docs", "ranking.png")
    img.save(output_path)
    print(f"✅ Imagem salva em {output_path}")

    # Gerar embed.html com cache-busting
    gerar_embed()

def gerar_embed():
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    html_code = f'<img src="https://raw.githubusercontent.com/mathpferreira/ranking-gta/main/docs/ranking.png?nocache={timestamp}" alt="Ranking GTA">'
    os.makedirs("docs", exist_ok=True)
    with open("docs/embed.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print("✅ embed.html gerado em docs/")

if __name__ == "__main__":
    main()
