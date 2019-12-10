import tushare as ts

pro = ts.pro_api('f3e484821271b2479be7885afa84b0be7f203209bcca903d890a4692')
data = pro.stock_basic()
print(data)
