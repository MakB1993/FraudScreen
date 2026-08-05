import { useEffect, useState } from "react";

import "../styles/Transactions.css";
import {
  getFraudEvaluations,
  getFraudEvaluationById,
} from "../services/fraudEvaluationsApi";

const PAGE_SIZE = 10;

function FraudEvaluations() {
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");
  const [filterError, setFilterError] = useState("");

  const [offset, setOffset] = useState(0);

  const [selectedEvaluation, setSelectedEvaluation] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState("");

  const [decision, setDecision] = useState("");
  const [decisionFilter, setDecisionFilter] = useState("");

  const [minScore, setMinScore] = useState("");
  const [minScoreFilter, setMinScoreFilter] = useState("");

  const [maxScore, setMaxScore] = useState("");
  const [maxScoreFilter, setMaxScoreFilter] = useState("");

  useEffect(() => {
    async function fetchFraudEvaluations() {
      try {
        setLoading(true);
        setError("");

        const data = await getFraudEvaluations(
          PAGE_SIZE,
          offset,
          {decision: decisionFilter,
            min_score: minScoreFilter,
            max_score: maxScoreFilter,
          }
        );

        setEvaluations(data);
      } catch (error) {
        console.error(
          "Failed to fetch fraud evaluations:",
          error
        );

        const message =
          error instanceof Error
            ? error.message
            : "Failed to fetch fraud evaluations";

        setError(message);
      } finally {
        setLoading(false);
      }
    }

    fetchFraudEvaluations();
  }, [offset, decisionFilter, minScoreFilter, maxScoreFilter]);

  function handleSearch() {
    setFilterError("");

    if (
      minScore &&
      maxScore &&
      Number(minScore) > Number(maxScore)
    ) {
      setFilterError("Min Score cannot be greater than Max Score.");
      return;
    }


    setOffset(0);
    setDecisionFilter(decision);
    setMinScoreFilter(minScore);
    setMaxScoreFilter(maxScore);
  }

  function handleClearFilters() {

    setFilterError("");
    setDecision("");
    setDecisionFilter("");
    
    setMinScore("");
    setMaxScore("");

    setMinScoreFilter("");
    setMaxScoreFilter("");

    setOffset(0);
  }

  function handlePrevious() {
    setOffset((currentOffset) =>
      Math.max(0, currentOffset - PAGE_SIZE)
    );

    setSelectedEvaluation(null);
    setDetailError("");
  }

  function handleNext() {
    setOffset((currentOffset) =>
      currentOffset + PAGE_SIZE
    );

    setSelectedEvaluation(null);
    setDetailError("");
  }

  async function handleView(id) {
    try {
      setDetailLoading(true);
      setDetailError("");

      const data = await getFraudEvaluationById(id);

      setSelectedEvaluation(data);
    } catch (error) {
      console.error(
        "Failed to load fraud evaluation:",
        error
      );

      const message =
        error instanceof Error
          ? error.message
          : "Failed to load fraud evaluation";

      setDetailError(message);
    } finally {
      setDetailLoading(false);
    }
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

  const sortedRuleEvaluations = [
    ...(selectedEvaluation?.rule_evaluations ?? []),
  ].sort(
    (a, b) =>
      Number(b.triggered) - Number(a.triggered)
  );

  const triggeredRuleCount =
    selectedEvaluation?.rule_evaluations?.filter(
      (rule) => rule.triggered
    ).length ?? 0;

  if (loading) {
    return <p>Loading fraud evaluations...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div className="table-container">
      <h2>Fraud Evaluations</h2>
        <form
          className="transaction-filters"
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch();
          }}
        >

          <div className="filter-field">
            <label>Decision</label>
            <select
              value={decision}
              onChange={(e) => setDecision(e.target.value)}
            >
              <option value="">All Decisions</option>
              <option value="APPROVE">APPROVE</option>
              <option value="REVIEW">REVIEW</option>
              <option value="REJECT">REJECT</option>
            </select>
          </div>
          
          <div className="filter-field">
            <label>Min Score</label>
            <input
              type="number"
              value={minScore}
              onChange={(e) => setMinScore(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>Max Score</label>
            <input
              type="number"
              value={maxScore}
              onChange={(e) => setMaxScore(e.target.value)}
            />
          </div>

          <button className="btn-primary" type="submit">
            Search
          </button>

          <button type="button" onClick={handleClearFilters}>
            Clear
          </button>

          {filterError && (
            <p className="filter-error">
              {filterError}
            </p>
          )}
        </form>

      {evaluations.length === 0 ? (
        <p>No fraud evaluations found.</p>
      ) : (
        <div className="table-scroll">
          <table className="transaction-table">
            <thead>
              <tr>
                <th>Evaluation ID</th>
                <th>Transaction ID</th>
                <th>Customer ID</th>
                <th>Amount</th>
                <th>Decision</th>
                <th>Total Score</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {evaluations.map((evaluation) => (
                <tr key={evaluation.id}>
                  <td>{evaluation.id}</td>

                  <td>
                    {evaluation.transaction.transaction_id}
                  </td>

                  <td>
                    {evaluation.transaction.customer_id}
                  </td>

                  <td>
                    {evaluation.transaction.amount}{" "}
                    {evaluation.transaction.currency}
                  </td>

                  <td>
                    <span
                      className={getDecisionClass(
                        evaluation.decision
                      )}
                    >
                      {evaluation.decision}
                    </span>
                  </td>

                  <td>{evaluation.total_score}</td>

                  <td>
                    {new Date(
                      evaluation.transaction.created_at
                    ).toLocaleString()}
                  </td>

                  <td>
                    <button
                      className="btn-primary"
                      onClick={() =>
                        handleView(evaluation.id)
                      }
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="pagination">
        <button
          onClick={handlePrevious}
          disabled={offset === 0}
        >
          Previous
        </button>

        <span>
          Page {offset / PAGE_SIZE + 1}
        </span>

        <button
          onClick={handleNext}
          disabled={evaluations.length < PAGE_SIZE}
        >
          Next
        </button>
      </div>

      {detailLoading && (
        <p>Loading evaluation details...</p>
      )}

      {detailError && (
        <p className="filter-error">
          {detailError}
        </p>
      )}

      {selectedEvaluation && !detailLoading && (
        <div className="fraud-details">
          <h3>Evaluation Details</h3>

          <p>
            <strong>Evaluation ID:</strong>{" "}
            {selectedEvaluation.id}
          </p>

          <p>
            <strong>Transaction ID:</strong>{" "}
            {
              selectedEvaluation.transaction
                .transaction_id
            }
          </p>

          <p>
            <strong>Customer ID:</strong>{" "}
            {
              selectedEvaluation.transaction
                .customer_id
            }
          </p>

          <p>
            <strong>Email:</strong>{" "}
            {selectedEvaluation.transaction.email}
          </p>

          <p>
            <strong>Amount:</strong>{" "}
            {selectedEvaluation.transaction.amount}{" "}
            {selectedEvaluation.transaction.currency}
          </p>

          <p>
            <strong>Decision:</strong>{" "}
            <span
              className={getDecisionClass(
                selectedEvaluation.decision
              )}
            >
              {selectedEvaluation.decision}
            </span>
          </p>

          <p>
            <strong>Total Score:</strong>{" "}
            {selectedEvaluation.total_score}
          </p>

          <p>
            <strong>Triggered Rules:</strong>{" "}
            {triggeredRuleCount}
          </p>

          <p>
            <strong>Created At:</strong>{" "}
            {new Date(
              selectedEvaluation.transaction.created_at
            ).toLocaleString()}
          </p>

          <h4>Rule Evaluations</h4>

          <table className="transaction-table">
            <thead>
              <tr>
                <th>Rule</th>
                <th>Triggered</th>
                <th>Score</th>
                <th>Reason</th>
              </tr>
            </thead>

            <tbody>
              {sortedRuleEvaluations.length === 0 ? (
                <tr>
                  <td colSpan={4}>
                    No rule evaluations available.
                  </td>
                </tr>
              ) : (
                sortedRuleEvaluations.map((rule) => (
                  <tr key={rule.id}>
                    <td>{rule.rule_name}</td>

                    <td>
                      {rule.triggered
                        ? "✅ Yes"
                        : "❌ No"}
                    </td>

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

export default FraudEvaluations;