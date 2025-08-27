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
def criar_frame(cor_titulo, cor2, cor3, top3):
    largura, altura = 600, 400
    img = Image.new("RGB", (largura, altura), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype("arialbd.ttf", 78)
        font_texto = ImageFont.truetype("arialbd.ttf", 62)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # --- Título ---
    titulo = "HALL DA FAMA"
    bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
    w = bbox[2] - bbox[0]
    x = (largura - w) / 2
    draw.text((x, 30), titulo, font=font_titulo, fill=cor_titulo)

    # --- Jogadores ---
    y = 150
    cores = [(218,165,32), cor2, cor3]  # ouro, prata, bronze
    for i, jogador in enumerate(top3):
        if len(jogador) < 2:
            continue
        nome, pontos = jogador[0], jogador[1]
        texto = f"{nome} - {pontos} pontos"
        bbox = draw.textbbox((0, 0), texto, font=font_texto)
        w = bbox[2] - bbox[0]
        x = (largura - w) / 2
        draw.text((x, y), texto, font=font_texto, fill=cores[i])
        y += 65
    return img

def main():
    # Dados de exemplo
    top3 = [
        ["Player1", "150"],
        ["Player2", "120"],
        ["Player3", "100"],
    ]

    # Cores RGB para o efeito
    ciclo_cores = [
        (255, 0, 0),    # vermelho
        (0, 255, 0),    # verde
        (0, 128, 255),  # azul
        (255, 0, 255),  # roxo
        (255, 165, 0),  # laranja
    ]

    frames = []
    for cor in ciclo_cores:
        frames.append(criar_frame(cor, (200,200,200), (176,141,87), top3))

    os.makedirs("docs", exist_ok=True)
    output_path = os.path.join("docs", "ranking.gif")

    # Salvar como GIF animado
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=500,  # ms por frame
        loop=0
    )

    print(f"✅ GIF animado salvo em {output_path}")

    # Atualizar embed
    gerar_embed()

def gerar_embed():
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    html_code = f'<img src="https://raw.githubusercontent.com/mathpferreira/ranking-gta/main/docs/ranking.gif?nocache={timestamp}" alt="Ranking GTA">'
    os.makedirs("docs", exist_ok=True)
    with open("docs/embed.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print("✅ embed.html atualizado para usar ranking.gif")

if __name__ == "__main__":
    main()
