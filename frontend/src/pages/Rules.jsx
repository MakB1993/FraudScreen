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

function Rules() {
  /** @type {[FraudRule[], Function]} */
  const [rules, setRules] = useState([]);

  useEffect(() => {
  fetch("http://127.0.0.1:8000/rules")
    .then((response) => response.json())
    .then((data) => {
      setRules(data);
    })
    .catch((error) => {
      console.error("Failed to fetch rules:", error);
    });
  }, []);

  return (
  <div>
    <h2>Rules</h2>

    {rules.map((rule) => (
      <p key={rule.rule_key}>{rule.rule_name}</p>
    ))}
  </div>
);
}

export default Rules;