from flask import Flask, request, render_template_string
import base64
import json
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Leitor de Contas</title>
</head>
<body>
    <h1>Envie a imagem da conta</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="imagem" accept="image/*">
        <button type="submit">Enviar</button>
    </form>
</body>
</html>
"""

HTML_RESULTADO = """
<!DOCTYPE html>
<html>
<head>
    <title>Resultado</title>
</head>
<body>
    <h1>Informações extraídas</h1>
    <ul>
        <li><strong>Valor da Conta:</strong> {valor}</li>
        <li><strong>Data de Referência:</strong> {data}</li>
        <li><strong>Consumo (kW):</strong> {consumo}</li>
        <li><strong>Concessionária:</strong> {concessionaria}</li>
    </ul>
    <a href="/">Enviar outra imagem</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        imagem = request.files.get("imagem")
        if imagem:
            try:
                img_bytes = imagem.read()
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")

                resposta = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        "Extraia as seguintes informações da conta de luz: "
                                        "valor da conta, data de referência, consumo em kW "
                                        "e nome da concessionária. Responda apenas com os dados em formato JSON válido, sem texto adicional."
                                    ),
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_b64}"
                                    },
                                },
                            ],
                        }
                    ],
                    temperature=0.2,
                    max_tokens=300,
                )

                conteudo = resposta.choices[0].message.content

                try:
                    dados = json.loads(conteudo)
                except json.JSONDecodeError:
                    return f"<p>Erro ao interpretar JSON da resposta:<br><pre>{conteudo}</pre></p>"

                return render_template_string(
                    HTML_RESULTADO,
                    valor=dados.get("valor", "Não encontrado"),
                    data=dados.get("data", "Não encontrado"),
                    consumo=dados.get("consumo", "Não encontrado"),
                    concessionaria=dados.get("concessionaria", "Não encontrado"),
                )
            except Exception as e:
                return f"<p>Erro ao processar imagem ou resposta da OpenAI: {e}</p>"

    return render_template_string(HTML_FORM)



