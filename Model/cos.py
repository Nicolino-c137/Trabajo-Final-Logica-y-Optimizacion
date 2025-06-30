from ibm_botocore.client import Config
from ibm_boto3 import client
from dotenv import load_dotenv
from collections import defaultdict
import pandas as pd
import os, csv

load_dotenv()
api_key= os.getenv("IBM_API_KEY")
cos_endpoint= os.getenv("COS_ENDPOINT")
cos_bucket= os.getenv("COS_BUCKET")
bucket_name= os.getenv("BUCKET_NAME")

cliente_cos= client("s3", 
    ibm_api_key_id= api_key, 
    ibm_service_instance_id= cos_bucket, 
    config=Config(signature_version="oauth"), 
    endpoint_url= cos_endpoint, 
)
        
def subir_archivo(archivo):
    cliente_cos.upload_file(archivo, Bucket= bucket_name, Key= archivo)
    
def get_solucion():    
    cliente_cos.download_file(bucket_name, "AllocationSolution.csv", "Solucion.csv")
    
def reescribir_csv(archivo):
    with open(archivo, "r", encoding= "utf-8") as archi:
        contenido= archi.readlines()
    delimitadores= [",", ";"]
    delimitador= max(delimitadores, key= lambda x: contenido[0].count(x))
    contenido= [linea.strip().split(delimitador) for linea in contenido]
    with open(archivo, "w", encoding= "utf-8", newline='') as archi:
        writer= csv.writer(archi, delimiter= ",")
        for linea in contenido:
            writer.writerow(linea)
    
def prepocesamiento():
    reescribir_csv("FlightLegs.csv")
    reescribir_csv("ItineraryLegs.csv")
    dfVuelos= pd.read_csv("FlightLegs.csv", sep= ",").to_dict(orient= "records")
    dfConexion= pd.read_csv("ItineraryLegs.csv", sep= ",").to_dict(orient= "records")
    id_vuelos= defaultdict(list)
    for dictConexion in dfConexion:
        id_vuelos[dictConexion["ItinID"]].append(dictConexion["FltID"])
    for clave, valor in id_vuelos.items():
        for vuelo in dfVuelos:
            if vuelo["FltID"] in valor:
                i= valor.index(vuelo["FltID"])
                valor[i]= [vuelo["Origin"], vuelo["Destination"]]
    return id_vuelos

def añadir_vuelos_solucion():
    relacion_vuelos= prepocesamiento() 
    df= pd.read_csv("Solucion.csv", sep= ",").to_dict(orient= "records")
    for itinerario in df:
        if int(itinerario["Itineraries.ItinID"]) in relacion_vuelos:
            itinerario["Vuelos"]= relacion_vuelos[int(itinerario["Itineraries.ItinID"])]
    df= pd.DataFrame(df)
    df.to_csv("Solucion.csv", sep= ",", index=False, encoding="utf-8")