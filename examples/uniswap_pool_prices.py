from handlers.UniswapV2 import UniswapV2
from utils.ERC20 import ERC20Handler


uni = UniswapV2()
data = uni.get_reserves("0xBb2b8038a1640196FbE3e38816F3e67Cba72D940")
print(f"ETHBTC Price: {(data['reserve1'] * 10 ** 18) / (data['reserve0'] * 10 ** 8)}")

erc20 = ERC20Handler()
print(erc20.get_decimals("0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"))
