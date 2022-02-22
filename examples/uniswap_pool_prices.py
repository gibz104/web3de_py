from handlers.UniswapV2 import UniswapV2
from utils.ERC20 import ERC20Handler

uni = UniswapV2()
erc20 = ERC20Handler()

# Set Uni v2 pool
unipool = "0xBb2b8038a1640196FbE3e38816F3e67Cba72D940"

# Get reserves of Uni v2 pool
reserves = uni.get_reserves(unipool)

# Get token addresses in Uni v2 pool
tokens = uni.get_pool_tokens(unipool)

# Get decimal places of tokens in Uni v2 pool
token0decimals = erc20.get_decimals(tokens['token0'])
token1decimals = erc20.get_decimals(tokens['token1'])

# Calculate exchange rate of the pool
pool_price = (reserves['reserve1'] * 10 ** token1decimals) / (reserves['reserve0'] * 10 ** token0decimals)

# print exchange rate
print(f"ETHBTC Price: {pool_price}")
