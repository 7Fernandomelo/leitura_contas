from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML simples com formulário para upload
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

# HTML com resultado simulado
HTML_RESULTADO = """
<!DOCTYPE html>
<html>
<head>
    <title>Resultado</title>
</head>
<body>
    <h1>Informações extraídas</h1>
    <ul>
        <li><strong>Valor da Conta:</strong> R$ 120,50</li>
        <li><strong>Data de Referência:</strong> 07/2025</li>
        <li><strong>Consumo (kW):</strong> 150</li>
        <li><strong>Concessionária:</strong> Eletropaulo</li>
    </ul>
    <a href="/">Enviar outra imagem</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Aqui futuramente você vai usar a imagem
        return render_template_string(HTML_RESULTADO)
    return render_template_string(HTML_FORM)

##if __name__ == "__main__":  app.run(debug=True)

