import React, { useState } from "react";
import axios from "axios";

function App() {
  const [form, setForm] = useState({
    buy_price: "",
    capital: "",
    target_profit_percent: ""
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const res = await axios.post("http://localhost:5000/calculate", {
        buy_price: parseFloat(form.buy_price),
        capital: parseFloat(form.capital),
        target_profit_percent: parseFloat(form.target_profit_percent || 0)
      });
      setResult(res.data);
    } catch (err) {
      alert("Something went wrong. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Stock Profit Calculator</h1>

      <div>
        <label>Buy Price (RM)</label>
        <input
          name="buy_price"
          type="number"
          step="0.01"
          value={form.buy_price}
          onChange={handleChange}
        />
      </div>

      <div>
        <label>Capital (RM)</label>
        <input
          name="capital"
          type="number"
          value={form.capital}
          onChange={handleChange}
        />
      </div>

      <div>
        <label>Target Profit (%)</label>
        <input
          name="target_profit_percent"
          type="number"
          step="0.1"
          value={form.target_profit_percent}
          onChange={handleChange}
          placeholder="Optional"
        />
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Calculating..." : "Calculate"}
      </button>

      {result && (
        <div>
          <div>Units to Buy: {result.units}</div>
          <div>Total Cost: RM {result.total_cost}</div>
          <div>Target Sell Price: RM {result.sell_price}</div>
          <div>Estimated Profit: RM {result.net_profit}</div>
        </div>
      )}
    </div>
  );
}

export default App;
