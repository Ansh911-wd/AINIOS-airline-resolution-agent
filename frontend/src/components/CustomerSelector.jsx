import { useEffect, useState } from "react";

const customers = [
  {
    name: "Priya Nair",
    loyalty_tier: "Gold",
    booking_reference: "SK4821X",
    issue: "Flight cancelled",
  },
  {
    name: "Arvind Kulkarni",
    loyalty_tier: "Silver",
    booking_reference: "TR1190B",
    issue: "4-hour delay",
  },
  {
    name: "Meher Kaur",
    loyalty_tier: "Platinum",
    booking_reference: "WL7742",
    issue: "6-hour delay",
  },
];

function CustomerSelector({ selectedCustomer, onCustomerChange }) {
  const [customersList, setCustomersList] = useState(customers);

  useEffect(() => {
    if (!selectedCustomer) {
      onCustomerChange(customers[0]);
    }
  }, []);

  return (
    <div className="card customer-card">
      <div className="section-title">
        <div>
          <h2>Customer</h2>
          <p>Select a disruption case</p>
        </div>
      </div>

      <div className="customer-list">
        {customersList.map((customer) => (
          <button
            key={customer.booking_reference}
            className={`customer-item ${
              selectedCustomer?.booking_reference ===
              customer.booking_reference
                ? "active"
                : ""
            }`}
            onClick={() => onCustomerChange(customer)}
          >
            <div className="avatar">
              {customer.name
                .split(" ")
                .map((word) => word[0])
                .join("")}
            </div>

            <div className="customer-info">
              <strong>{customer.name}</strong>

              <span>
                {customer.loyalty_tier} · {customer.booking_reference}
              </span>

              <small>{customer.issue}</small>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default CustomerSelector;