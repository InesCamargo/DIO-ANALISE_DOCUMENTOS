from fastapi import FastAPI, UploadFile
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

app = FastAPI()

endpoint = "https://analisedocumentos.cognitiveservices.azure.com/"
key = "KEY"

client = DocumentAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

@app.post("/extrair")
async def extrair(file: UploadFile):
    conteudo = await file.read()
    poller = client.begin_analyze_document("prebuilt-document", conteudo)
    result = poller.result()

    secoes = []

    for p in result.paragraphs:
        if p.role == "title":
            secoes.append({"tipo": "titulo", "conteudo": p.content})
        elif p.role == "sectionHeading":
            secoes.append({"tipo": "secao", "conteudo": p.content})
        else:
            secoes.append({"tipo": "paragrafo", "conteudo": p.content})

    return {"secoes": secoes}
