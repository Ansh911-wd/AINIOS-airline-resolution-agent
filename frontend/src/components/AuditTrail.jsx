function AuditTrail({ result }) {
  if (!result) {
    return (
      <div className="card">
        <div className="section-title">
          <div>
            <h2>Audit Trail</h2>
            <p>Conversation and action record</p>
          </div>
        </div>

        <div className="policy-placeholder">
          Actions will be recorded here.
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="section-title">
        <div>
          <h2>Audit Trail</h2>
          <p>Resolution activity</p>
        </div>
      </div>

      <div className="audit-list">
        <div className="audit-item">
          <span className="audit-dot"></span>

          <div>
            <strong>Customer identified</strong>
            <p>
              {result.customer.name} ·{" "}
              {result.customer.booking_reference}
            </p>
          </div>
        </div>

        <div className="audit-item">
          <span className="audit-dot"></span>

          <div>
            <strong>Intent extracted</strong>
            <p>
              {result.intent.intent?.join(", ") ||
                "Disruption request"}
            </p>
          </div>
        </div>

        <div className="audit-item">
          <span className="audit-dot"></span>

          <div>
            <strong>Policy evaluated</strong>
            <p>
              {result.decision.decisions.length} decision(s)
              generated
            </p>
          </div>
        </div>

        <div className="audit-item">
          <span className="audit-dot"></span>

          <div>
            <strong>Resolution completed</strong>
            <p>{result.decision.final_status}</p>
          </div>
        </div>

        {result.decision.escalation_required && (
          <div className="audit-item escalation-audit">
            <span className="audit-dot"></span>

            <div>
              <strong>Supervisor escalation required</strong>
              <p>
                Agent authority limit exceeded.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AuditTrail;