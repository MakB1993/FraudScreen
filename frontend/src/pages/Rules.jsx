/**
 * @typedef {Object} FraudRule
 * @property {number} id
 * @property {string} rule_key
 * @property {string} rule_name
 * @property {boolean} enabled
 * @property {number} threshold_value
 * @property {number} score
 * @property {number|null} window_minutes
 */

import { useEffect, useState } from "react";
// import { data } from "react-router-dom";

import "../styles/Rules.css"
import { getRules, updateRule } from "../services/rulesApi";

function Rules() {
  /** @type {[FraudRule[], Function]} */
  const [rules, setRules] = useState([]);
  
  const [selectedRule, setSelectedRule] = useState(
    /** @type {FraudRule | null} */ (null)
  );

  const [editForm, setEditForm] = useState({
    threshold_value: 0,
    score: 0,
    enabled: false,
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
  async function fetchRules() {
    

    try {
      setLoading(true);
      setError("");

      const data = await getRules();

      setRules(data);
    } catch (error) {
      console.error("Failed to fetch rules:", error);

      const message =
        error instanceof Error
          ? error.message
          : "Failed to fetch rules";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  fetchRules();
}, []);
    
  

  /**
 * @param {FraudRule} rule
 */
  function handleEdit(rule) {
    setSelectedRule(rule);

    setEditForm({
      threshold_value: rule.threshold_value,
      score: rule.score,
      enabled: rule.enabled,
    });
  }

  
  async function handleSave() {
    if (!selectedRule) return;
    setSaving(true);
    try{
    const updatedRule = await updateRule(selectedRule.rule_key,editForm);

    setRules((currentRules) =>
      currentRules.map((rule) =>
        rule.rule_key === updatedRule.rule_key
          ? updatedRule
          : rule
      )
    );

    setSelectedRule(null);

    }catch (error) {
      console.error(error);
      const message =
        error instanceof Error
          ? error.message
          : "Failed to update rule";

      alert(message);
      
    }
    finally {
      setSaving(false);
    }
    
  }

  if (loading) {
    return <p>Loading rules...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (rules.length === 0) {
    return <p>No rules found.</p>;
  }

  return (
  <div className="table-container">
    <h2>Rules</h2>

    <table className="rules-table">
      <thead>
        <tr>
          <th>Id</th>
          <th>Rule Name</th>
          <th>Rule Key</th>
          <th>Status</th>
          <th>Threshold</th>
          <th>Score</th>
          <th>Window</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        {rules.map((rule) => (
          <tr key={rule.id}>
            <td>{rule.id}</td>
            <td>{rule.rule_name}</td>
            <td>{rule.rule_key}</td>
            <td>
              <span className={rule.enabled ? "status enabled" : "status disabled"}
              >
              {rule.enabled ? "Enabled" : "Disabled"}
              </span>
            </td>
            <td>{rule.threshold_value}</td>
            <td>{rule.score}</td>
            <td>
              {rule.window_minutes != null
                ? `${rule.window_minutes} minutes`
                : "Not applicable"}
            </td>
            <td>
              <button onClick={() => handleEdit(rule)}>
                Edit
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    {selectedRule && (
      <div className="modal-overlay">
        <div className="edit-modal">
          <h3>Edit Rule</h3>

          <p>
            <strong>{selectedRule.rule_name}</strong>
          </p>

          <label>
            Threshold
          </label>
          <input
            type="number"
            value={editForm.threshold_value}
            onChange={(e) =>
              setEditForm({
                ...editForm,
                threshold_value: Number(e.target.value),
              })
            }
          />
          <label>
            Score
          </label>

          <input
            type="number"
            value={editForm.score}
            onChange={(e) =>
              setEditForm({
                ...editForm,
                score: Number(e.target.value),
              })
            }
          />

          <label>
            <input
              type="checkbox"
              checked={editForm.enabled}
              onChange={(e) =>
                setEditForm({
                  ...editForm,
                  enabled: e.target.checked,
                })
              }
            />
            Enabled
          </label>

          <button onClick={handleSave} disabled={saving}>
            {saving ? "Saving..." : "Save"}
          </button>

          <button onClick={() => setSelectedRule(null)}
            disabled={saving}
          >
            Cancel
          </button>
        </div>
      </div>
    )}
  </div>
);
}

export default Rules;