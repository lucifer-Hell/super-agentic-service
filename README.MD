| Module             | Purpose                                           | Example Classes / Files                                           |
| ------------------ | ------------------------------------------------- | ----------------------------------------------------------------- |
| **core/**          | Core interfaces, base abstractions                | `AgentBase`, `ToolBase`, `WorkflowBase`, `LLMBase`, `StorageBase` |
| **agents/**        | Custom agent implementations                      | `ChatAgent`, `RetrievalAgent`, `ControllerAgent`                  |
| **tools/**         | Custom tools (search, retrieval, math, API calls) | `WebSearchTool`, `DatabaseQueryTool`, etc.                        |
| **workflows/**     | LangGraph workflow definitions                    | `customer_support_graph.py`, `data_enrichment_graph.py`           |
| **llm_providers/** | LLM integration adapters                          | `OpenAIProvider`, `ClaudeProvider`, `LocalModelProvider`          |
| **storage/**       | Storage abstraction + implementations             | `SQLiteStorage`, `MemoryStorage`, `MilvusStorage`                 |
| **service/**       | API or CLI layer to expose workflows              | `workflow_server.py`, `app.py`                                    |
| **config/**        | YAML/JSON-based configuration management          | `config.yaml`                                                     |
| **tests/**         | Unit + integration tests                          | `test_agents.py`, `test_workflows.py`                             |

## Calling the Talk API

To invoke the chat workflow, use the following curl command:

```bash
curl -X POST "http://localhost:8000/v1/talk" \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "query": "hi there"
    },
    "conversationId": "CHAT123",
    "requestAttributes": {
      "flows": {
        "entry": {
          "ref": "CHAT_FLOW"
        }
      }
    }
  }'
```

This will send a request to the /v1/talk endpoint with the required payload structure.
