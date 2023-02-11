import logging

import azure.functions as func
from azure.storage.blob import BlobClient


def display_blob(conn_string):
    
    blob_client = BlobClient.from_blob_url(conn_string)
    download_blob = blob_client.download_blob()
    logging.info('==============')
    logging.info(download_blob.readall())
    logging.info('==============')

def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> str:
    conn_string='https://functionstorageyoutube.blob.core.windows.net/function-app-example/function-app-data.txt?sp=r&st=2023-02-05T15:51:54Z&se=2023-02-05T23:51:54Z&spr=https&sv=2021-06-08&sr=b&sig=HhjAqj2XLYqJQppeUPNhb4S%2B0JZmL4yxXD9uZirAP2U%3D'
    display_blob(conn_string)
        
    input_data = req.params.get('input')
    if not input_data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input_data = req_body.get('input')

    if input_data:
        msg.set(input_data)
        return func.HttpResponse(f"Hello {input_data}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )
    
        