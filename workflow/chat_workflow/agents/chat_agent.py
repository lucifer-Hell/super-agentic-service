from workflow.chat_workflow.tools.retrieve_info import retrieve_info

class ChatAgent:
    """
    Chat agent that answers queries using the retrieve_info tool.
    """
    def __init__(self, domain: str):
        self.domain = domain

    def answer(self, query: str):
        chunks = retrieve_info(self.domain, query)
        # Simple answer formulation: concatenate chunks
        answer = "\n".join(chunks)
        return answer

