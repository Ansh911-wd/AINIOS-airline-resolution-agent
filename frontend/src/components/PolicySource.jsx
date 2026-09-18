function PolicySource({ result }) {
  if (!result) {
    return (
      <div className="card">
        <div className="section-title">
          <div>
            <h2>Policy Sources</h2>
            <p>Rules used by the decision engine</p>
          </div>
        </div>

        <div className="policy-placeholder">
          Policy evidence will appear after resolution.
        </div>
      </div>
    );
  }

  const sources = [
    ...new Set(
      result.decision.decisions.map(
        (decision) => decision.source
      )
    ),
  ];

  return (
    <div className="card">
      <div className="section-title">
        <div>
          <h2>Policy Sources</h2>
          <p>Evidence behind the decision</p>
        </div>
      </div>

      <div className="policy-list">
        {sources.map((source, index) => (
          <div className="policy-item" key={index}>
            <span>📋</span>
            <span>{source}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PolicySource;