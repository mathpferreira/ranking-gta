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

    # Pega o Top 3 (ignora cabeçalho)
    top3 = [linha.split(",") for linha in linhas[1:4]]

    # Criar imagem
    largura, altura = 600, 400
    img = Image.new("RGB", (largura, altura), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype("arialbd.ttf", 36)  # versão bold
        font_texto = ImageFont.truetype("arialbd.ttf", 28)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # --- Título ---
    titulo = "TOP3 RANKING - EQUIPE DE EVENTOS"
    bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
    w = bbox[2] - bbox[0]

    # Sombra do título
    draw.text(((largura - w) / 2 + 2, 32), titulo, font=font_titulo, fill=(20, 20, 20))
    draw.text(((largura - w) / 2, 30), titulo, font=font_titulo, fill=(101, 138, 106))

    # --- Jogadores ---
    y = 120
    cores = [(218, 165, 32), (215, 215, 215), (176, 141, 87)]  # ouro, prata, bronze
    for i, jogador in enumerate(top3):
        if len(jogador) < 2:
            continue
        nome, pontos = jogador[0], jogador[1]
        texto = f"{nome} - {pontos} pontos"

        # Fake bold se não tiver arialbd.ttf
        for dx in (0, 1):
            for dy in (0, 1):
                draw.text((80 + dx, y + dy), texto, font=font_texto, fill=cores[i])

        y += 50  # espaçamento menor entre linhas

    # Salvar imagem dentro de docs/
    os.makedirs("docs", exist_ok=True)
    output_path = os.path.join("docs", "ranking.png")
    img.save(output_path)
    print(f"✅ Imagem salva em {output_path}")

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
