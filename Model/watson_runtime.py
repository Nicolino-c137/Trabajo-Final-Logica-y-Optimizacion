from ibm_watsonx_ai import APIClient, Credentials
from dotenv import load_dotenv
import os, time

load_dotenv()
api_key= os.getenv("IBM_API_KEY")
bucket_name= os.getenv("BUCKET_NAME")
watson_endpoint= os.getenv("WATSON_ENDPOINT")
deploy_id= os.getenv("DEPLOY_ID")
deployment_id= os.getenv("DEPLOYMENT_ID")
connection_id= os.getenv("CONNECTION_ID")

credenciales= Credentials(
    api_key= api_key,
    url= watson_endpoint 
)

cliente_watson= APIClient(credenciales, space_id= deploy_id)

job_payload= {
    "input_data_references": [
        {
            "type": "connection_asset",
            "connection": {
                "id": connection_id,
            },
            "id": "Itineraries.csv",
            "location": {
                "bucket": bucket_name,
                "file_name": "Itineraries.csv"
            }
        },
        {
            "type": "connection_asset",
            "connection": {
                "id": connection_id,
            },
            "id": "FlightLegs.csv",
            "location": {
                "bucket": bucket_name,
                "file_name": "FlightLegs.csv"
            }
        },
        {
            "type": "connection_asset",
            "connection": {
                "id": connection_id,
            },
            "id": "ItineraryLegs.csv",
            "location": {
                "bucket": bucket_name,
                "file_name": "ItineraryLegs.csv"
            }
        }
    ],
    "output_data_references": [
        {
            "type": "connection_asset",
            "connection": {
                "id": connection_id,
            },
            "id": "AllocationSolution.csv",
            "location": {
                "bucket": bucket_name,
                "file_name": "AllocationSolution.csv"
            }
        }
    ]
}

def ejecutar_modelo():
    job= cliente_watson.deployments.create_job(deployment_id= deployment_id, meta_props= job_payload)
    job_id= job["metadata"]["id"]
    while True:
        estado= cliente_watson.deployments.get_job_status(job_id)
        print(f"Estado del job: {estado["state"]}")
        if estado["state"] in ["completed", "failed"]:
            break
        time.sleep(5)