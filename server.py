from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from get_model import salvar_arquivo_ifc
from html_dynamic import get_html
from fastapi import FastAPI
import base64
import uvicorn
import uuid
import io
import os


app = FastAPI()
api_endpoint = 'http://localhost:8000/loader'


@app.get("/{url_encode}", response_class=HTMLResponse)
def main(url_encode: str):
    return get_html(api_endpoint=api_endpoint, url_encode=url_encode)


@app.get("/loader/{url_encode}")
def read_root(url_encode: str):
    url_encode += '=' * (-len(url_encode) % 4)
    url_decode_bytes = base64.urlsafe_b64decode(url_encode)
    url_decode = url_decode_bytes.decode('utf-8')
    
    path_token = f'{uuid.uuid4()}'
    
    if salvar_arquivo_ifc(path=path_token, url=url_decode):
        with open(f"{path_token}.glb", "rb") as f:
            arquivo_memoria = io.BytesIO(f.read())
            arquivo_memoria.seek(0)
            f.close()
            
        os.system(f'rm -rf {path_token}.glb {path_token}.ifc')
        
        return StreamingResponse(
            arquivo_memoria,
            media_type="model/gltf-binary",
            headers={"Content-Disposition": "attachment; filename=modelo.glb"}
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Usa variável de ambiente para definir a porta
    uvicorn.run(app, host="0.0.0.0", port=port)