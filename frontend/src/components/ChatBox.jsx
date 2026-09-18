import { useState } from "react";

function ChatBox({ customer, onResolve, loading, result }) {
  const [message, setMessage] = useState("");
  const [submittedMessage, setSubmittedMessage] = useState("");

  const exampleMessages = {
    SK4821X:
      "My flight was cancelled. I want a full refund and I also want a free business class upgrade on my return flight.",

    TR1190B:
      "My flight is delayed by 4 hours. Can you provide hotel accommodation?",

    WL7742:
      "My flight is delayed by 6 hours. I want a full night's hotel stay and I want to change to a higher-fare flight. The fare difference is 2000 rupees.",
  };

  const handleExample = () => {
    if (customer) {
      setMessage(
        exampleMessages[customer.booking_reference] || ""
      );
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!message.trim() || loading) return;

    const currentMessage = message.trim();

    setSubmittedMessage(currentMessage);

    await onResolve(currentMessage);
  };

  const formatResponse = (text) => {
    if (!text) return null;

    return text.split("\n").map((line, index) => {
      let formatted = line;

      formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
      );

      formatted = formatted.replace(
        /^\* (.*)/,
        "• $1"
      );

      return (
        <div
          key={index}
          dangerouslySetInnerHTML={{
            __html: formatted || "&nbsp;",
          }}
        />
      );
    });
  };

  return (
    <div className="card chat-card">

      <div className="section-title">
        <div>
          <h2>Customer Conversation</h2>

          <p>
            {customer
              ? `${customer.name} · ${customer.booking_reference}`
              : "Select a customer"}
          </p>
        </div>

        <button
          className="example-button"
          onClick={handleExample}
          disabled={!customer || loading}
        >
          Load Example
        </button>
      </div>

      <div className="chat-area">

        {!result && !submittedMessage ? (
          <div className="empty-chat">
            <div className="empty-icon">💬</div>

            <h3>Ready to assist</h3>

            <p>
              Enter the customer's request below or load
              the example scenario.
            </p>
          </div>
        ) : (
          <>
            {submittedMessage && (
              <div className="message customer-message">
                <div className="message-label">
                  {customer?.name}
                </div>

                <p>{submittedMessage}</p>
              </div>
            )}

            {loading && (
              <div className="message agent-message">
                <div className="message-label">
                  Resolution Agent
                </div>

                <p className="typing">
                  🤖 Analyzing request and applying policy...
                </p>
              </div>
            )}

            {result && (
              <div className="message agent-message">
                <div className="message-label">
                  Resolution Agent
                </div>

                <div className="agent-response">
                  {formatResponse(result.customer_response)}
                </div>
              </div>
            )}
          </>
        )}

      </div>

      <form onSubmit={handleSubmit} className="chat-form">

        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder={
            customer
              ? "Type the customer's request..."
              : "Select a customer first..."
          }
          disabled={!customer || loading}
        />

        <button
          type="submit"
          className="resolve-button"
          disabled={
            !customer ||
            !message.trim() ||
            loading
          }
        >
          {loading
            ? "Resolving..."
            : "Resolve Request →"}
        </button>

      </form>

    </div>
  );
}

export default ChatBox;