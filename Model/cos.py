from ibm_botocore.client import Config, ClientError
from ibm_boto3 import client
from dotenv import load_dotenv
import os

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