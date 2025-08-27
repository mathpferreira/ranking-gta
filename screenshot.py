from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
import os
import csv
import re
from io import StringIO
from datetime import datetime


def main():
    # URL do CSV do Google Sheets
    url = "https://docs.google.com/spreadsheets/d/1DS24AMuYnkEJTDVaNHeAB1gGEoz6YOew4IckQD7JjOw/export?format=csv&gid=0"
    response = requests.get(url)
    response.encoding = "utf-8"

    # ---- Parse CSV e ordenar por pontos (desc) ----
    rows = list(csv.reader(StringIO(response.text)))
    # Remove linhas vazias
    rows = [r for r in rows if r and any(c.strip() for c in r)]

    if not rows or len(rows) < 2:
        raise ValueError("CSV sem dados suficientes.")

    header = [c.strip().lower() for c in rows[0]]
    # Tenta achar colunas pelo nome; fallback para as 2 primeiras
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
        # extrai só dígitos (ex.: "1.200" -> "1200")
        num = re.sub(r"[^\d]", "", bruto)
        pontos = int(num) if num else 0
        if nome:
            dados.append((nome, pontos))

    # Ordena do maior para o menor
    dados.sort(key=lambda x: x[1], reverse=True)
    top3 = dados[:3]

    # ---- Criar imagem base (RGBA para suportar glow) ----
    largura, altura = 600, 400
    img = Image.new("RGBA", (largura, altura), (30, 30, 30, 255))
    draw = ImageDraw.Draw(img)

    # Fontes
    try:
        font_titulo = ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", 22)
        font_texto = ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", 16)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # ---- Título (centralizado, stroke para "engrossar" sem borrar) ----
    titulo = ""
    bbox_t = draw.textbbox((0, 0), titulo, font=font_titulo, stroke_width=2)
    w_t = bbox_t[2] - bbox_t[0]
    x_t = (largura - w_t) / 2
    y_t = 24
    draw.text(
        (x_t, y_t),
        titulo,
        font=font_titulo,
        fill=(101, 138, 106, 255),       # verde
        stroke_width=2,
        stroke_fill=(15, 15, 15, 255),   # contorno escuro
    )

    # ---- Lista de jogadores (centralizados) ----
    y = 60  # menos espaço entre título e lista
    cores = [
        (218, 165, 32, 255),   # ouro #DAA520
        (215, 215, 215, 255),  # prata #D7D7D7
        (176, 141, 87, 255),   # bronze #B08D57
    ]
    posicoes = ["1", "2", "3"]

    for i, (nome, pontos) in enumerate(top3):
        texto = f"{posicoes[i]} {nome} - {pontos} pontos"

        # centralizar cada linha
        bbox = draw.textbbox((0, 0), texto, font=font_texto)
        w = bbox[2] - bbox[0]
        x = (largura - w) / 2

        if i == 0:
            # ---- Glow SUAVE atrás do TOP 1 (sem borrar o texto principal) ----
            glow_layer = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow_layer)
            # escreve o texto numa cor dourada com alpha (só para o glow)
            glow_draw.text((x, y), texto, font=font_texto, fill=(255, 215, 0, 180))
            # aplica blur para espalhar o brilho
            glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=8))
            # compõe na base
            img = Image.alpha_composite(img, glow_layer)
            draw = ImageDraw.Draw(img)  # recria o draw na imagem resultante

        # Texto principal (nítido)
        draw.text((x, y), texto, font=font_texto, fill=cores[i])

        # espaçamento ainda menor entre linhas
        y += 20

    # ---- Salvar imagem ----
    os.makedirs("docs", exist_ok=True)
    output_path = os.path.join("docs", "ranking.png")
    img.save(output_path)
    print(f"✅ Imagem salva em {output_path}")

    # ---- Gerar embed.html com cache-busting ----
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
