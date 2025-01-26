import requests
import io
import os


def baixar_arquivo_memoria(url):
    resposta = requests.get(url, stream=True)
    if resposta.status_code == 200:
        buffer = io.BytesIO()
        for chunk in resposta.iter_content(chunk_size=8192):
            buffer.write(chunk)
        buffer.seek(0)  # Retorna o cursor para o início do buffer
        return buffer
    else:
        raise Exception(f"Erro ao baixar arquivo. Código: {resposta.status_code}")


def salvar_arquivo_ifc(path, url):
    try:
        print(f"Arquivo salvo em: {os.path.abspath(f'{path}.ifc')}")
        
        lines = []
        for line in list(baixar_arquivo_memoria(url).readlines()):
            lines.append(f'{line.decode()}')
            
        with open(path+'.ifc', 'w') as FileW:
            FileW.writelines(lines)
            FileW.close()
        os.system(f'/app/IfcConvert /app/{path}.ifc /app/{path}.glb')
        
        return True
            
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")