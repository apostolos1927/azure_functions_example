import logging
import azure.functions as func
from azure.storage.blob import BlobClient


def display_blob(conn_string):

    blob_client = BlobClient.from_blob_url(conn_string)
    download_blob = blob_client.download_blob()
    logging.info("==============")
    logging.info(download_blob.readall())
    logging.info("==============")


def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    conn_string = "<Place your SAS URL from the item located in Blob Storage>"
    display_blob(conn_string)

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        msg.set(name)
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400,
        )
