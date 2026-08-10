/**
 * @typedef {Object} FraudRule
 * @property {number} id
 * @property {string} rule_key
 * @property {string} rule_name
 * @property {boolean} enabled
 * @property {number} threshold_value
 * @property {number|boolean|null} comparison_value
 * @property {number} score
 * @property {number|null} window_minutes
 * @property {string|null} signal_key
 * @property {string|null} operator
 */

import { useEffect, useState } from "react";
// import { data } from "react-router-dom";

import "../styles/Rules.css"
import { getRules, updateRule } from "../services/rulesApi";

import { getSignals } from "../services/signalsApi";

function Rules() {
  /** @type {[FraudRule[], Function]} */
  const [rules, setRules] = useState([]);
  const [signals, setSignals] = useState({});
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  const [selectedRule, setSelectedRule] = useState(
    /** @type {FraudRule | null} */ (null)
  );

  const [createForm, setCreateForm] = useState({
    rule_name: "",
    signal_key: "",
    operator: "",
    comparison_value: null,
    score: 0,
    window_minutes: null,
    enabled: true,
  });

  const [editForm, setEditForm] = useState({
    signal_key: "",
    operator: "",
    threshold_value: 0,
    comparison_value: null,
    score: 0,
    enabled: false,
    window_minutes: null,
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);


  useEffect(() => {

  async function fetchSignals() {
    try {
      const data = await getSignals();
      setSignals(data);
    } catch (error) {
      console.error("Failed to fetch signals:", error);
    }
  }

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
  fetchSignals();
}, []);
    
  
  /**
 * @param {FraudRule} rule
 */
  function handleEdit(rule) {
    setSelectedRule(rule);

    setEditForm({
      signal_key: rule.signal_key || "",
      operator: rule.operator || "",
      threshold_value: rule.threshold_value,
      comparison_value: rule.comparison_value,
      score: rule.score,
      enabled: rule.enabled,
      window_minutes: rule.window_minutes,
    });
  }

  
  async function handleSave() {
    if (!selectedRule) return;
    setSaving(true);
    try{
      const selectedSignal = signals[editForm.signal_key];

      if (
        !selectedSignal?.allowed_operators?.includes(editForm.operator)
      ) {
        alert("Please select a valid operator for the selected signal.");
        setSaving(false);
        return;
      }

      const payload = {
        ...editForm,
        window_minutes: selectedSignal?.uses_window
          ? editForm.window_minutes
          : null,
      };
      const updatedRule = await updateRule(selectedRule.rule_key, payload);

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

  const selectedSignalDefinition = signals[editForm.signal_key];
  const selectedCreateSignal = signals[createForm.signal_key];

  return (
  <>
    <button onClick={() => setShowCreateModal(true)}>
      Create Rule
    </button>

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
              <span
                className={
                  rule.enabled
                    ? "status enabled"
                    : "status disabled"
                }
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

    {/* =========================
        CREATE RULE MODAL
       ========================= */}

    {showCreateModal && (
      <div className="modal-overlay">
        <div className="edit-modal">
          <h3>Create Rule</h3>

          <label>Rule Name</label>

          <input
            type="text"
            value={createForm.rule_name}
            onChange={(e) =>
              setCreateForm({
                ...createForm,
                rule_name: e.target.value,
              })
            }
          />

          <label>Signal</label>

          <select
            value={createForm.signal_key}
            onChange={(e) =>
              setCreateForm({
                ...createForm,
                signal_key: e.target.value,
              })
            }
          >
            <option value="">Select signal</option>

            {Object.entries(signals).map(
              ([signalKey, definition]) => (
                <option
                  key={signalKey}
                  value={signalKey}
                >
                  {definition.display_name}
                </option>
              )
            )}
          </select>

          <label>Operator</label>

          <select
            value={createForm.operator}
            onChange={(e) =>
              setCreateForm({
                ...createForm,
                operator: e.target.value,
              })
            }
            disabled={!selectedCreateSignal}
          >
            <option value="">Select operator</option>

            {selectedCreateSignal?.allowed_operators?.map(
              (operator) => (
                <option
                  key={operator}
                  value={operator}
                >
                  {operator}
                </option>
              )
            )}
          </select>

          {selectedCreateSignal && (
            <>
              <label>Comparison Value</label>

              {selectedCreateSignal.data_type ===
              "boolean" ? (
                <select
                  value={
                    createForm.comparison_value === null
                      ? ""
                      : String(
                          createForm.comparison_value
                        )
                  }
                  onChange={(e) =>
                    setCreateForm({
                      ...createForm,
                      comparison_value:
                        e.target.value === ""
                          ? null
                          : e.target.value === "true",
                    })
                  }
                >
                  <option value="">
                    Select value
                  </option>

                  <option value="true">
                    True
                  </option>

                  <option value="false">
                    False
                  </option>
                </select>
              ) : (
                <input
                  type="number"
                  value={
                    createForm.comparison_value ?? ""
                  }
                  onChange={(e) =>
                    setCreateForm({
                      ...createForm,
                      comparison_value:
                        e.target.value === ""
                          ? null
                          : Number(e.target.value),
                    })
                  }
                />
              )}

              {selectedCreateSignal.uses_window && (
                <>
                  <label>
                    Window Minutes
                  </label>

                  <input
                    type="number"
                    min="1"
                    value={
                      createForm.window_minutes ?? ""
                    }
                    onChange={(e) =>
                      setCreateForm({
                        ...createForm,
                        window_minutes:
                          e.target.value === ""
                            ? null
                            : Number(e.target.value),
                      })
                    }
                  />
                </>
              )}
            </>
          )}

          <button
            onClick={() =>
              setShowCreateModal(false)
            }
          >
            Cancel
          </button>
        </div>
      </div>
    )}

    {/* =========================
        EDIT RULE MODAL
       ========================= */}

    {selectedRule && (
      <div className="modal-overlay">
        <div className="edit-modal">
          <h3>Edit Rule</h3>

          <p>
            <strong>
              {selectedRule.rule_name}
            </strong>
          </p>

          <label>
            Signal
          </label>

          <select
            value={editForm.signal_key}
            onChange={(e) =>
              setEditForm({
                ...editForm,
                signal_key: e.target.value,
              })
            }
          >
            <option value="">
              Select signal
            </option>

            {Object.entries(signals).map(
              ([signalKey, definition]) => (
                <option
                  key={signalKey}
                  value={signalKey}
                >
                  {definition.display_name}
                </option>
              )
            )}
          </select>

          <label>
            Operator
          </label>

          <select
            value={editForm.operator}
            onChange={(e) =>
              setEditForm({
                ...editForm,
                operator: e.target.value,
              })
            }
          >
            <option value="">
              Select operator
            </option>

            {signals[
              editForm.signal_key
            ]?.allowed_operators?.map(
              (operator) => (
                <option
                  key={operator}
                  value={operator}
                >
                  {operator}
                </option>
              )
            )}
          </select>

          <label>
            Comparison Value
          </label>

          {selectedSignalDefinition?.data_type ===
          "boolean" ? (
            <select
              value={
                editForm.comparison_value === null
                  ? ""
                  : String(
                      editForm.comparison_value
                    )
              }
              onChange={(e) =>
                setEditForm({
                  ...editForm,
                  comparison_value:
                    e.target.value === ""
                      ? null
                      : e.target.value === "true",
                })
              }
            >
              <option value="">
                Select value
              </option>

              <option value="true">
                True
              </option>

              <option value="false">
                False
              </option>
            </select>
          ) : (
            <input
              type="number"
              value={
                editForm.comparison_value ?? ""
              }
              onChange={(e) =>
                setEditForm({
                  ...editForm,
                  comparison_value:
                    e.target.value === ""
                      ? null
                      : Number(e.target.value),
                })
              }
            />
          )}

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

          {signals[
            editForm.signal_key
          ]?.uses_window && (
            <>
              <label>
                Window Minutes
              </label>

              <input
                type="number"
                min="1"
                value={
                  editForm.window_minutes ?? ""
                }
                onChange={(e) =>
                  setEditForm({
                    ...editForm,
                    window_minutes:
                      e.target.value === ""
                        ? null
                        : Number(e.target.value),
                  })
                }
              />
            </>
          )}

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

          <button
            onClick={handleSave}
            disabled={saving}
          >
            {saving
              ? "Saving..."
              : "Save"}
          </button>

          <button
            onClick={() =>
              setSelectedRule(null)
            }
            disabled={saving}
          >
            Cancel
          </button>
        </div>
      </div>
    )}
  </>
);
}

export default Rules;