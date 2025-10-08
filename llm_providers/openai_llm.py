import os
import ssl

import httpx
from langchain_openai import AzureChatOpenAI

context = ssl.create_default_context()
context.load_verify_locations(os.getenv("SSL_CERTIFICATE_PATH"))

custom_headers = {
    "x-api-key": os.getenv("OPENAI_API_KEY"),
    "Content-Type": "application/json",
}
http_client = httpx.Client(verify=context, headers=custom_headers)

llm = AzureChatOpenAI(
                    model=os.getenv("LLM_MODEL"),
                    api_key=os.getenv("OPENAI_API_KEY"),
                    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
                    api_version=os.getenv("API_VERSION"),
                    http_client=http_client
)

# llm.bind_tools(all_tools,tool_choice="required", strict = True)