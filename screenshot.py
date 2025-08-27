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

   # Paleta RGB para o brilho do título
    cores_rgb = [(255, 0, 0), (0, 255, 0), (0, 120, 255), (255, 0, 255)]

    frames = []
    for frame_idx, cor in enumerate(cores_rgb):
        img = Image.new("RGB", (largura, altura), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)

        # --- Título ---
        titulo = "HALL DA FAMA"
        bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
        w = bbox[2] - bbox[0]
        # Brilho (camada "embaçada" atrás do texto)
        draw.text(((largura - w) / 2, 40), titulo, font=font_titulo, fill=cor)
        # Título branco por cima
        draw.text(((largura - w) / 2, 40), titulo, font=font_titulo, fill=(255, 255, 255))

        # --- Jogadores ---
        y = 150
        cores = [(218, 165, 32), (215, 215, 215), (176, 141, 87)]  # ouro, prata, bronze
        for i, jogador in enumerate(top3):
            if len(jogador) < 2:
                continue
            nome, pontos = jogador[0], jogador[1]
            texto = f"{nome} - {pontos} pontos"

            bbox = draw.textbbox((0, 0), texto, font=font_texto)
            w = bbox[2] - bbox[0]

            # Aplica brilho pulsante no 2º e 3º
            if i > 0:
                glow = tuple(min(255, c + frame_idx*40) for c in cores[i])  # aumenta brilho
                draw.text(((largura - w) / 2, y), texto, font=font_texto, fill=glow)

            # Nome principal
            draw.text(((largura - w) / 2, y), texto, font=font_texto, fill=cores[i])
            y += 70

        frames.append(img)

    # Salvar como GIF animado
    os.makedirs("docs", exist_ok=True)
    output_path = os.path.join("docs", "ranking.gif")
    frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=True, duration=500, loop=0)
    print(f"✅ GIF animado salvo em {output_path}")

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
