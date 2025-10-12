# Models based on provided schemas
class ClientUser:
    def __init__(self, id: str):
        self.id = id

class ClientInfo:
    def __init__(self, domainId: str, channelId: str, conversationId: str, user: ClientUser):
        self.domainId = domainId
        self.channelId = channelId
        self.conversationId = conversationId
        self.user = user

class RetrieverRequest:
    def __init__(self, client: ClientInfo, query: str, context: Optional[dict] = None, appContext: Optional[List[str]] = None, experiments: Optional[Dict[str, Any]] = None):
        self.client = client
        self.query = query
        self.context = context
        self.appContext = appContext or []
        self.experiments = experiments or {}
