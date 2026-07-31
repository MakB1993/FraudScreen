import { useEffect, useState } from "react";

import "../styles/Transactions.css";
import { getTransactions } from "../services/transactionsApi";
import { getFraudEvaluation } from "../services/fraudEvaluationApi";

const PAGE_SIZE = 10;

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [fraudEvaluation, setFraudEvaluation] = useState(null);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    async function fetchTransactions() {
      try {
        setLoading(true);
        setError("");

        const data = await getTransactions(PAGE_SIZE, offset);
        setTransactions(data);
      } catch (error) {
        console.error("Failed to fetch transactions:", error);

        const message =
          error instanceof Error
            ? error.message
            : "Failed to fetch transactions";

        setError(message);
      } finally {
        setLoading(false);
      }
    }

    fetchTransactions();
  }, [offset]);

  function handlePrevious() {
    setOffset((currentOffset) =>
      Math.max(0, currentOffset - PAGE_SIZE)
    );
  }

  function handleNext() {
    setOffset((currentOffset) => currentOffset + PAGE_SIZE);
  }

  async function handleView(transaction) {
    try {
      const data = await getFraudEvaluation(transaction.transaction_id);

      console.log("Fraud evaluation response:", data);

      setSelectedTransaction(transaction);
      setFraudEvaluation(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load fraud evaluation");
    }
  }

  if (loading) {
    return <p>Loading transactions...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  function getDecisionClass(decision) {
    switch (decision) {
      case "APPROVE":
        return "decision approve";
      case "REVIEW":
        return "decision review";
      case "REJECT":
        return "decision reject";
      default:
        return "decision";
    }
  }

  return (
    <div className="table-container">
      <h2>Transactions</h2>

      {transactions.length === 0 ? (
        <p>No transactions found.</p>
      ) : (
        <table className="transaction-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Transaction ID</th>
              <th>Customer ID</th>
              <th>Email</th>
              <th>Card BIN</th>
              <th>Last 4</th>
              <th>IP Address</th>
              <th>Device ID</th>
              <th>Amount</th>
              <th>Currency</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td>{transaction.id}</td>
                <td>{transaction.transaction_id}</td>
                <td>{transaction.customer_id}</td>
                <td>{transaction.email}</td>
                <td>{transaction.card_bin}</td>
                <td>{transaction.card_last_four}</td>
                <td>{transaction.ip_address}</td>
                <td>{transaction.device_id}</td>
                <td>{transaction.amount}</td>
                <td>{transaction.currency}</td>
                <td>
                  {new Date(transaction.created_at).toLocaleString()}
                </td>
                <td>
                  <button onClick={() => handleView(transaction)}>
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="pagination">
        <button
          onClick={handlePrevious}
          disabled={offset === 0}
        >
          Previous
        </button>

        <span>Page {offset / PAGE_SIZE + 1}</span>

        <button
          onClick={handleNext}
          disabled={transactions.length < PAGE_SIZE}
        >
          Next
        </button>
      </div>

      {selectedTransaction && fraudEvaluation && (
        <div className="fraud-details">
          <h3>Fraud Evaluation</h3>

          <p>
            <strong>Transaction:</strong>{" "}
            <span className={getDecisionClass(fraudEvaluation.decision)}>
              {fraudEvaluation.decision}
            </span>
          </p>

          <p>
            <strong>Decision:</strong>{" "}
            {fraudEvaluation.decision}
          </p>

          <p>
            <strong>Total Score:</strong>{" "}
            {fraudEvaluation.total_score}
          </p>

          <h4>Rule Evaluations</h4>

          <table>
            <thead>
              <tr>
                <th>Rule</th>
                <th>Triggered</th>
                <th>Score</th>
                <th>Reason</th>
              </tr>
            </thead>

            <tbody>
              {(fraudEvaluation.rule_evaluations ?? []).length === 0 ? (
                <tr>
                  <td colSpan={4}>No rule evaluations available.</td>
                </tr>
              ) : (
                fraudEvaluation.rule_evaluations.map((rule) => (
                  <tr key={rule.id}>
                    <td>{rule.rule_name}</td>
                    <td>{rule.triggered ? "✅ Yes" : "❌ No"}</td>
                    <td>{rule.score}</td>
                    <td>{rule.reason}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Transactions;