import { useEffect, useState } from "react";

import "../styles/Transactions.css";
import { getTransactions, getTransactionFraudEvaluation } from "../services/transactionsApi";

const PAGE_SIZE = 10;

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [fraudEvaluation, setFraudEvaluation] = useState(null);
  const [offset, setOffset] = useState(0);

  const [transactionId, setTransactionId] = useState("");
  const [transactionIdFilter, setTransactionIdFilter] = useState("");

  const [customerId, setCustomerId] = useState(""); // what we are typing in box
  const [customerIdFilter, setCustomerIdFilter] = useState(""); //what we are actually searching for

  const [email, setEmail] = useState("");
  const [emailFilter, setEmailFilter] = useState("");

  const [deviceId, setDeviceId] = useState("");
  const [deviceIdFilter, setDeviceIdFilter] = useState("");

  const [ipAddress, setIPAddress] = useState("");
  const [ipAddressFilter, setIPAddressFilter] = useState("");

  const [minAmount, setMinAmount] = useState("");
  const [minAmountFilter, setMinAmountFilter] = useState("");

  const [maxAmount, setMaxAmount] = useState("");
  const [maxAmountFilter, setMaxAmountFilter] = useState("");

  const [currency, setCurrency] = useState("");
  const [currencyFilter, setCurrencyFilter] = useState("");

  const [startDate, setStartDate] = useState("");
  const [startDateFilter, setStartDateFilter] = useState("");

  const [endDate, setEndDate] = useState("");
  const [endDateFilter, setEndDateFilter] = useState("");

  const [filterError, setFilterError] = useState("");


  useEffect(() => {
    async function fetchTransactions() {
      try {
        setLoading(true);
        setError("");

        const data = await getTransactions(PAGE_SIZE, offset, {customer_id: customerIdFilter,
          email: emailFilter,
          device_id: deviceIdFilter,
          ip_address: ipAddressFilter,
          min_amount: minAmountFilter,
          max_amount: maxAmountFilter,
          currency: currencyFilter,
          start_date: startDateFilter,
          end_date: endDateFilter,
          transaction_id: transactionIdFilter,
        });
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
  }, [offset, customerIdFilter, 
      emailFilter, deviceIdFilter, 
      ipAddressFilter, 
      minAmountFilter, maxAmountFilter,
      currencyFilter, startDateFilter, 
      endDateFilter, transactionIdFilter,
  ]);

  function handleSearch() {
    setFilterError("");

    if (
      minAmount &&
      maxAmount &&
      Number(minAmount) > Number(maxAmount)
    ) {
      setFilterError("Min Amount cannot be greater than Max Amount.");
      return;
    }

    if (
      startDate &&
      endDate &&
      startDate > endDate
    ) {
      setFilterError("Invalid Date Range");
      return;
    }

    setOffset(0);
    setTransactionIdFilter(transactionId);
    setCustomerIdFilter(customerId);
    setEmailFilter(email);
    setDeviceIdFilter(deviceId);
    setIPAddressFilter(ipAddress);
    setMinAmountFilter(minAmount);
    setMaxAmountFilter(maxAmount);
    setCurrencyFilter(currency);
    setStartDateFilter(startDate);
    setEndDateFilter(endDate);
  }

  function handleClearFilters() {
    setFilterError("");
    setTransactionId("");
    setCustomerId("");
    setEmail("");
    setDeviceId("");
    setIPAddress("");
    setCurrency("");

    setCustomerIdFilter("");
    setEmailFilter("");
    setDeviceIdFilter("");
    setIPAddressFilter("");
    setCurrencyFilter("");
    setTransactionIdFilter("");

    setMinAmount("");
    setMaxAmount("");

    setMinAmountFilter("");
    setMaxAmountFilter("");

    setStartDate("");
    setEndDate("");

    setStartDateFilter("");
    setEndDateFilter("");

    setOffset(0);
  }

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
      const data = await getTransactionFraudEvaluation(transaction.transaction_id);

      console.log("Fraud evaluation response:", data);

      setSelectedTransaction(transaction);
      setFraudEvaluation(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load fraud evaluation");
    }
  }

  const triggeredRuleCount =
    fraudEvaluation?.rule_evaluations?.filter(
      (rule) => rule.triggered
    ).length ?? 0;

  const sortedRuleEvaluations =
  [...(fraudEvaluation?.rule_evaluations ?? [])]
    .sort(
      (a, b) =>
        Number(b.triggered) - Number(a.triggered)
    );

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
        <form
          className="transaction-filters"
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch();
          }}
        >
          <div className="filter-field">
            <label>Transaction ID</label>
            <input
              type="text"
              value={transactionId}
              onChange={(e) => setTransactionId(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>Customer ID</label>
            <input
              type="text"
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>Email</label>
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>Device ID</label>
            <input
              type="text"
              value={deviceId}
              onChange={(e) => setDeviceId(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>IP Address</label>
            <input
              type="text"
              value={ipAddress}
              onChange={(e) => setIPAddress(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>Min Amount</label>
            <input
              type="number"
              value={minAmount}
              onChange={(e) => setMinAmount(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>Max Amount</label>
            <input
              type="number"
              value={maxAmount}
              onChange={(e) => setMaxAmount(e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label>Currency</label>
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
            >
              <option value="">All Currencies</option>
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
              <option value="INR">INR</option>
              <option value="AUD">AUD</option>
            </select>
          </div>

          <div className="filter-field">
            <label>Date Range</label>
            <div className="date-range-filter">
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />

              <span>to</span>

              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
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

      {transactions.length === 0 ? (
        <p>No transactions found.</p>
      ) : (
        <div className="table-scroll">
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
                    <button className="btn-primary"
                      onClick={() => handleView(transaction)}>
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
            {selectedTransaction.transaction_id}
          </p>

          <p>
            <strong>Evaluation ID:</strong>{" "}
            {fraudEvaluation.id}
          </p>

          <p>
            <strong>Decision:</strong>{" "}
            <span className={getDecisionClass(fraudEvaluation.decision)}>
              {fraudEvaluation.decision}
            </span>
          </p>

          <p>
            <strong>Total Score:</strong>{" "}
            {fraudEvaluation.total_score}
          </p>

          <p>
            <strong>Triggered Rules:</strong>{" "}
            {triggeredRuleCount}
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
              {sortedRuleEvaluations.length === 0 ? (
                <tr>
                  <td colSpan={4}>No rule evaluations available.</td>
                </tr>
              ) : (
                sortedRuleEvaluations.map((rule) => (
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