import requests
import json

# Use http://localhost:8545/graphql/ui for interactive window
api = "http://localhost:8545/graphql"

# Returns pending transactions
pending_txs = """
{
  pending{
    transactionCount
    transactions {
      hash
      from {
        address
      }
      to {
        address
      }
      value
      inputData
    }
  }
}
"""

resp = requests.post(api, json={'query': pending_txs})
parsed = json.loads(resp.text)
print(json.dumps(parsed, indent=2, sort_keys=True))

