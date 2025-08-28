from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
import os
import csv
import re
from io import StringIO
from datetime import datetime
import random


def main():
    # URL do CSV do Google Sheets
    url = "https://docs.google.com/spreadsheets/d/1DS24AMuYnkEJTDVaNHeAB1gGEoz6YOew4IckQD7JjOw/export?format=csv&gid=0"
    response = requests.get(url)
    response.encoding = "utf-8"

    # ---- Parse CSV e ordenar por pontos (desc) ----
    rows = list(csv.reader(StringIO(response.text)))
    rows = [r for r in rows if r and any(c.strip() for c in r)]

    if not rows or len(rows) < 2:
        raise ValueError("CSV sem dados suficientes.")

    header = [c.strip().lower() for c in rows[0]]
    try:
        idx_nome = header.index("nome")
    except ValueError:
        idx_nome = 0
    try:
        idx_pontos = header.index("pontos")
    except ValueError:
        idx_pontos = 1

    dados = []
    for r in rows[1:]:
        if len(r) <= max(idx_nome, idx_pontos):
            continue
        nome = r[idx_nome].strip()
        bruto = r[idx_pontos].strip()
        num = re.sub(r"[^\d]", "", bruto)
        pontos = int(num) if num else 0
        if nome:
            dados.append((nome, pontos))

    dados.sort(key=lambda x: x[1], reverse=True)
    top3 = dados[:3]

    # ---- Criar imagem base ----
    largura, altura = 460, 150
    img = Image.new("RGBA", (largura, altura), color=(30, 30, 30, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", 22)
        font_texto = ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", 18)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # ---- Título ----
    titulo = ""
    bbox_t = draw.textbbox((0, 0), titulo, font=font_titulo, stroke_width=2)
    w_t = bbox_t[2] - bbox_t[0]
    x_t = (largura - w_t) / 2
    y_t = 24
    draw.text(
        (x_t, y_t),
        titulo,
        font=font_titulo,
        fill=(101, 138, 106, 255),
        stroke_width=2,
        stroke_fill=(15, 15, 15, 255),
    )

    # ---- Lista jogadores ----
    y = 50
    cores = [(218, 165, 32), (215, 215, 215), (176, 141, 87)]
    for i, jogador in enumerate(top3):
        if len(jogador) < 2:
            continue
        nome, pontos = jogador
        texto = f"{i+1}º {nome} - {pontos} pontos"

        bbox = draw.textbbox((0, 0), texto, font=font_texto)
        w = bbox[2] - bbox[0]
        x = (largura - w) / 2

        cor = cores[i]
        draw.text((x+2, y+2), texto, font=font_texto, fill=(0, 0, 0, 150))
        draw.text((x, y), texto, font=font_texto, fill=cor)

        y += 20

    # ---- Forçar mudança invisível ----
    rand_alpha = random.randint(0, 255)
    img.putpixel((largura-1, altura-1), (0, 0, 0, rand_alpha))

    # ---- Salvar imagem ----
    os.makedirs("docs", exist_ok=True)
    output_path = os.path.join("docs", "ranking.png")
    img.save(output_path, "PNG")
    print(f"✅ Imagem salva em {output_path}")

    gerar_embed()


def gerar_embed():
    html_code = '<img src="https://raw.githubusercontent.com/mathpferreira/ranking-gta/main/docs/ranking.png" alt="Ranking GTA">'
    os.makedirs("docs", exist_ok=True)
    with open("docs/embed.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print("✅ embed.html gerado em docs/")


if __name__ == "__main__":
    main()
