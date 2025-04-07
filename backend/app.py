from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_trade():
    data = request.json
    buy_price = data['buy_price']
    capital = data['capital']
    target_profit = data.get('target_profit_percent', 0)

    units = int(capital // (buy_price * 100)) * 100
    total_buy = units * buy_price

    stamp_buy = math.ceil(total_buy * 0.001)
    clearing_buy = total_buy * 0.0003
    sst_buy = clearing_buy * 0.06
    total_fees_buy = stamp_buy + clearing_buy + sst_buy
    total_cost = total_buy + total_fees_buy

    target_total = total_cost * (1 + target_profit / 100)

    def net_proceeds(sell_price):
        gross = sell_price * units
        stamp = math.ceil(gross * 0.001)
        clearing = gross * 0.0003
        sst = clearing * 0.06
        return gross - (stamp + clearing + sst)

    sell_price = buy_price
    while net_proceeds(sell_price) < target_total:
        sell_price += 0.005

    net_profit = net_proceeds(sell_price) - total_cost

    return jsonify({
        "units": units,
        "total_cost": round(total_cost, 2),
        "sell_price": round(sell_price, 3),
        "net_profit": round(net_profit, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
