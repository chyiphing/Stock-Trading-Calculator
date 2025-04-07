from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    buy_price = data.get('buy_price')
    capital = data.get('capital')
    target_profit_percent = data.get('target_profit_percent', 0)
    
    # Calculate the units to buy
    units = capital / buy_price
    
    # Calculate the target sell price based on the target profit percentage
    target_sell_price = buy_price * (1 + target_profit_percent / 100)
    
    # Calculate the total cost and profit
    total_cost = buy_price * units
    net_profit = (target_sell_price * units) - total_cost
    
    result = {
        "units": units,
        "total_cost": total_cost,
        "sell_price": target_sell_price,
        "net_profit": net_profit
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
