from PIL import Image, ImageDraw, ImageFont
import requests, re, json

def main():
    # 🔹 Troque pelo ID da sua planilha
    SHEET_ID = "SUA_PLANILHA_ID"
    # Aqui pedimos apenas colunas E, F e G (top3 já pronto)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tq=select+E,F,G+limit+3"

    res = requests.get(url)
    match = re.search(r"google.visualization.Query.setResponse\((.+)\)", res.text)
    data = json.loads(match.group(1))

    rows = data["table"]["rows"]

    # Monta lista com Top 3 (cada linha é Jogador, Pontos, Ranking)
    top3 = []
    for row in rows:
        jogador = row["c"][0]["v"] if row["c"][0] else ""
        pontos = row["c"][1]["v"] if row["c"][1] else ""
        posicao = row["c"][2]["v"] if row["c"][2] else ""
        top3.append(f"{posicao}º - {jogador} ({pontos} pts)")

    # 🔹 Cria imagem base
    largura, altura = 500, 220
    img = Image.new("RGB", (largura, altura), color="white")
    draw = ImageDraw.Draw(img)

    # Fonte
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 28)
        font_texto = ImageFont.truetype("arial.ttf", 22)
    except:
        font_titulo = ImageFont.load_default()
        font_texto = ImageFont.load_default()

    # Título
    y = 20
    draw.text((largura//2 - 120, y), "🏆 TOP 3 RANKING 🏆", font=font_titulo, fill="black")

    # Lista
    y += 60
    for linha in top3:
        draw.text((50, y), linha, font=font_texto, fill="black")
        y += 40

    img.save("ranking.png")
    print("✅ Imagem gerada: ranking.png")

if __name__ == "__main__":
    main()
