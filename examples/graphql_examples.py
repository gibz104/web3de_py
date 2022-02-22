import json
import requests

# Use http://localhost:8545/graphql/ui for interactive window
api = "http://localhost:8545/graphql"

# Returns latest blocks and block attributes
blocks = """
{
  block {
    transactionCount
    number
    hash
    miner {
      address
    }
  }
}
"""

resp = requests.post(api, json={'query': blocks})
parsed = json.loads(resp.text)
print(json.dumps(parsed, indent=2, sort_keys=True))

# Returns transactions in latest block
transactions = """
{
  block {
    transactionCount
    number
    hash
    miner {
      address
    }
    transactions {
      index
      maxFeePerGas
      maxPriorityFeePerGas
      status
      gasUsed
      cumulativeGasUsed
      effectiveGasPrice
      type
    }
  }
}
"""

resp = requests.post(api, json={'query': transactions})
parsed = json.loads(resp.text)
print(json.dumps(parsed, indent=2, sort_keys=True))

# Returns storage slot from specific address
storage_slot = """
{
  block {
    account(address: "0xBb2b8038a1640196FbE3e38816F3e67Cba72D940") {
      address
      balance
      transactionCount
      code
      storage(slot: "0x0000000000000000000000000000000000000000000000000000000000000008")
    }
  }
}
"""

resp = requests.post(api, json={'query': storage_slot})
parsed = json.loads(resp.text)
print(json.dumps(parsed, indent=2, sort_keys=True))


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


# Gas estimate
gasEstimate = """
{
  gasPrice
}
"""

resp = requests.post(api, json={'query': gasEstimate})
parsed = json.loads(resp.text)
print(json.dumps(parsed, indent=2, sort_keys=True))
