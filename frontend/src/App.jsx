import { useState } from "react";
import CustomerSelector from "./components/CustomerSelector";
import ChatBox from "./components/ChatBox";
import DecisionPanel from "./components/DecisionPanel";
import PolicySource from "./components/PolicySource";
import AuditTrail from "./components/AuditTrail";
import "./index.css";


const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleResolve = async (message) => {
    if (!selectedCustomer) {
      alert("Please select a customer first.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/resolve`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          pnr: selectedCustomer.booking_reference,
          message,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Resolution failed");
      }

      setResult(data);
    } catch (error) {
      console.error(error);
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCustomerChange = (customer) => {
    setSelectedCustomer(customer);
    setResult(null);
  };

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>✈️ AINIOS Resolution Agent</h1>
          <p>AI-powered customer disruption resolution</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Agent Online
        </div>
      </header>

      <main className="dashboard">

        {/* LEFT SIDE */}
        <section className="left-column">

          <CustomerSelector
            selectedCustomer={selectedCustomer}
            onCustomerChange={handleCustomerChange}
          />

          <ChatBox
            customer={selectedCustomer}
            onResolve={handleResolve}
            loading={loading}
            result={result}
          />

        </section>

        {/* RIGHT SIDE */}
        <section className="right-column">

          <DecisionPanel
            result={result}
            loading={loading}
          />

          <PolicySource
            result={result}
          />

          <AuditTrail
            result={result}
          />

        </section>

      </main>
    </div>
  );
}

export default App;