from PIL import Image, ImageDraw, ImageFont
import requests, re, json

def main():
    SHEET_ID = "1DS24AMuYnkEJTDVaNHeAB1gGEoz6YOew4IckQD7JjOw"
    # Pega diretamente as colunas E, F e G (Top 3 já pronto na planilha)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tq=select+E,F,G+limit+3"

    res = requests.get(url)
    match = re.search(r"google.visualization.Query.setResponse\((.+)\)", res.text)
    data = json.loads(match.group(1))

    rows = data["table"]["rows"]
    top3 = []
    for row in rows:
        jogador = row["c"][0]["v"] if row["c"][0] else ""
        pontos = row["c"][1]["v"] if row["c"][1] else ""
        ranking = row["c"][2]["v"] if row["c"][2] else ""
        top3.append(f"{ranking}º - {jogador} ({pontos} pts)")

    largura, altura = 500, 220
    img = Image.new("RGB", (largura, altura), "white")
    draw = ImageDraw.Draw(img)

    try:
        font_titulo = ImageFont.truetype("arial.ttf", 28)
        font_texto = ImageFont.truetype("arial.ttf", 22)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # --- título centralizado ---
    y = 20
    titulo = "🏆 TOP 3 RANKING 🏆"
    bbox = draw.textbbox((0, 0), titulo, font=font_titulo)  # calcula box do texto
    w_titulo = bbox[2] - bbox[0]
    draw.text(((largura - w_titulo) / 2, y), titulo, font=font_titulo, fill="black")

    # --- lista ---
    y += 60
    for linha in top3:
        draw.text((50, y), linha, font=font_texto, fill="black")
        y += 40

    img.save("ranking.png")
    print("✅ Imagem atualizada: ranking.png")

if __name__ == "__main__":
    main()
