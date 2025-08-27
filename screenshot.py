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

    # Pegando apenas o Top 3
    top3 = [linha.split(",") for linha in linhas[1:4]]  # ignora cabeçalho

    # Criar imagem
    largura, altura = 600, 400
    img = Image.new("RGB", (largura, altura), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype("arial.ttf", 36)
        font_texto = ImageFont.truetype("arial.ttf", 28)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # Título
    titulo = "🏆 TOP 3 RANKING 🏆"
    bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
    w = bbox[2] - bbox[0]
    draw.text(((largura - w) / 2, 30), titulo, font=font_titulo, fill=(255, 215, 0))

    # Escrever os jogadores
    y = 120
    medalhas = ["🥇", "🥈", "🥉"]
    for i, jogador in enumerate(top3):
        if len(jogador) < 2:
            continue
        nome, pontos = jogador[0], jogador[1]
        texto = f"{medalhas[i]} {nome} - {pontos} pts"
        draw.text((80, y), texto, font=font_texto, fill=(255, 255, 255))
        y += 70

    # Salvar imagem
    output_path = os.path.join(os.getcwd(), "ranking.png")
    img.save(output_path)
    print(f"✅ Imagem salva em {output_path}")

    # Gerar embed.html
    gerar_embed()

def gerar_embed():
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    # usa o raw.githubusercontent (sempre instantâneo)
    img_url = f"https://raw.githubusercontent.com/mathpferreira/ranking-gta/main/ranking.png?nocache={timestamp}"
    html_code = f'<img src="{img_url}" alt="Ranking GTA">'
    with open("embed.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print("✅ embed.html gerado com código atualizado!")

if __name__ == "__main__":
    main()
