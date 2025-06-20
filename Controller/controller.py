from fastapi import APIRouter, UploadFile, HTTPException
from Model import cos, watson_runtime
import os

router= APIRouter()

@router.post("/subir_archivo")
async def cargar_archivo(archivo: UploadFile):
    if not archivo.filename.endswith(".csv"):
        raise HTTPException(status_code= 400, detail= "Formato de archivo no soportado")
    with open(archivo.filename, "wb") as archi:
        archi.write(await archivo.read())
    cos.subir_archivo(archivo.filename)
    return {"Mensaje": "Archivo cargado exitosamente"}

@router.post("/ejecutar_modelo")
def ejecutar_modelo():
    watson_runtime.ejecutar_modelo()
    return {"Mensaje": "Modelo ejecutado exitosamente"}

@router.get("/obtener_solucion")
def obtener_solucion():
    cos.get_solucion()
    return {"Mensaje": "Solución obtenida exitosamente"}

@router.delete("/borrar_archivo_local/{archivo}")
def eliminar_archivo(archivo: str):
    try:
        print(archivo)
        os.remove(archivo)
        return {"Mensaje": "Archivo eliminado exitosamente"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el archivo")