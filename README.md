# API pessoal de remoção de fundo de imagem

API simples, 100% gratuita, que recebe um **link de imagem** e devolve a imagem com o fundo removido (PNG com transparência). Feita para você usar como serviço de apoio nos seus outros projetos (via chamada HTTP com sua API key).

Usa a biblioteca `rembg` (modelo `u2netp`, leve) — não depende de nenhuma API paga (sem OpenAI, sem remove.bg, sem custo por imagem).

## 1. Subir para o GitHub

```bash
cd remove-bg-api
git init
git add .
git commit -m "primeira versão da API de remoção de fundo"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/remove-bg-api.git
git push -u origin main
```

## 2. Deploy no Render (plano free)

1. Entre em render.com e faça login com o GitHub.
2. New → Blueprint → selecione esse repositório (ele já detecta o `render.yaml`).
3. Quando pedir a variável `API_KEY`, defina uma chave só sua (ex: uma string aleatória grande). É ela que vai proteger a API.
4. Clique em "Apply" e espere o build terminar (alguns minutos, porque baixa o `onnxruntime`).

Sua API vai ficar em algo como: `https://remove-bg-api-xxxx.onrender.com`

### Sobre o plano free do Render
- 750 horas de instância grátis por mês, 512MB de RAM — por isso o projeto usa o modelo `u2netp`, que é leve.
- O serviço "dorme" depois de um tempo sem uso e demora uns 30-60s pra acordar na primeira chamada seguinte. Isso é normal e não custa nada.

## 3. Como usar (em qualquer um dos seus projetos)

**Requisição:**
```
GET https://SEU-APP.onrender.com/remove-bg?url=LINK_DA_IMAGEM&api_key=SUA_CHAVE
```

Ou com a chave no header (mais seguro que deixar na URL):
```
GET https://SEU-APP.onrender.com/remove-bg?url=LINK_DA_IMAGEM
Header: x-api-key: SUA_CHAVE
```

**Resposta:** a imagem PNG já sem fundo (bytes da imagem direto, não é JSON).

### Exemplo em Python
```python
import requests
r = requests.get(
    "https://SEU-APP.onrender.com/remove-bg",
    params={"url": "https://exemplo.com/foto.jpg", "api_key": "SUA_CHAVE"}
)
with open("saida.png", "wb") as f:
    f.write(r.content)
```

### No Sketchware Pro (Soundly / Social Play)
Use o componente de conexão HTTP (ou WebView) do Sketchware apontando pra essa URL com a imagem que você já tem hospedada; a resposta é o PNG pronto pra usar como capa/avatar sem fundo.

## Testar localmente antes de subir
```bash
pip install -r requirements.txt
API_KEY=teste123 python app.py
# depois, em outra aba:
curl "http://localhost:5000/remove-bg?url=https://exemplo.com/foto.jpg&api_key=teste123" -o saida.png
```
