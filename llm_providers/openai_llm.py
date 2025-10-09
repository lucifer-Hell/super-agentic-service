import os
import ssl
from dotenv import load_dotenv

load_dotenv()

import httpx
from langchain_openai import AzureChatOpenAI

cert_path = os.getenv("SSL_CERTIFICATE_PATH")
if not cert_path:
    raise RuntimeError("SSL_CERTIFICATE_PATH environment variable is not set. Please check your .env file.")

context = ssl.create_default_context()
context.load_verify_locations(cert_path)

custom_headers = {
    "x-api-key": os.getenv("OPENAI_API_KEY"),
    "Content-Type": "application/json",
    "WM_CONSUMER.ID": "a439ec1d-6c3c-4b95-b134-b84c293ef841",
    "WM_SVC.NAME": "WMTLLMGATEWAY",
    "WM_SVC.ENV": "stage"
}
http_client = httpx.Client(verify=context, headers=custom_headers)
async_client = httpx.AsyncClient(verify=context, headers=custom_headers)

llm = AzureChatOpenAI(
                    model=os.getenv("LLM_MODEL"),
                    api_key=os.getenv("OPENAI_API_KEY"),
                    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
                    api_version=os.getenv("API_VERSION"),
                    http_client=http_client,
                    async_client=async_client
)

# llm.bind_tools(all_tools,tool_choice="required", strict = True)