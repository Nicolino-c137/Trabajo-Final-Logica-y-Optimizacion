from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from Model import cos, watson_runtime
import os
import pandas as pd


router= APIRouter()

@router.post("/subir_archivo")
async def cargar_archivo(archivo: UploadFile):
    if not archivo.filename.endswith(".csv"):
        raise HTTPException(status_code= 400, detail= "Formato de archivo no soportado")
    with open(archivo.filename, "wb") as archi:
        archi.write(await archivo.read())
    cos.subir_archivo(archivo.filename)
    return {"Mensaje": "Archivo cargado exitosamete"}

@router.post("/ejecutar_modelo")
def ejecutar_modelo():
    watson_runtime.ejecutar_modelo()

@router.get("/obtener_solucion")
def obtener_solucion():
    cos.get_solucion()
    cos.prepocesamiento()
    cos.añadir_vuelos_solucion()
    return {"Mensaje": "Solución obtenida exitosamente"}

@router.get("/ver_solucion")
def ver_solucion():
    try:
        df = pd.read_csv("Solucion.csv")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo de solución no encontrado")
    
@router.get("/descargar_solucion")
def descargar_solucion():
    archivo = "Solucion.csv"
    if os.path.exists(archivo):
        return FileResponse(archivo, filename="Solucion.csv", media_type="text/csv")
    else:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

@router.delete("/borrar_archivo_local/{archivo}")
def eliminar_archivo(archivo: str):
    try:
        os.remove(archivo)
        return {"Mensaje": "Archivo eliminado exitosamente"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el archivo")