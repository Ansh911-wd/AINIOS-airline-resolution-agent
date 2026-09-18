function DecisionPanel({ result, loading }) {
  if (loading) {
    return (
      <div className="card">
        <div className="section-title">
          <div>
            <h2>Decision</h2>
            <p>Agent is evaluating the request...</p>
          </div>
        </div>

        <div className="loading-box">
          🤖 Analyzing customer intent and applying policy...
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="card">
        <div className="section-title">
          <div>
            <h2>Decision</h2>
            <p>Policy-grounded resolution</p>
          </div>
        </div>

        <div className="empty-panel">
          Resolution decisions will appear here.
        </div>
      </div>
    );
  }

  const decision = result.decision;

  return (
    <div className="card">
      <div className="section-title">
        <div>
          <h2>Decision</h2>
          <p>Policy-grounded resolution</p>
        </div>

        <span
          className={`status-badge ${
            decision.escalation_required
              ? "escalation"
              : "resolved"
          }`}
        >
          {decision.final_status}
        </span>
      </div>

      <div className="decision-list">
        {decision.decisions.map((item, index) => (
          <div className="decision-item" key={index}>
            <div className="decision-main">
              <strong>
                {item.action.replaceAll("_", " ")}
              </strong>

              <span
                className={`decision-status ${item.status
                  .toLowerCase()
                  .replaceAll(" ", "-")}`}
              >
                {item.status}
              </span>
            </div>

            <p>{item.reason}</p>

            <small>
              Source: {item.source}
            </small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DecisionPanel;