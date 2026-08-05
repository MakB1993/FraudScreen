import { useEffect, useState } from "react";
import { getDashboardSummary, getTransactionsOverTime } from "../services/dashboardApi";

import "../styles/Dashboard.css";

import {
  PieChart,
  Pie,
  Tooltip,
  Sector,
  ResponsiveContainer,
  Legend,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const DECISION_COLORS = {
  Approved: "#22c55e",
  Review: "#eab308",
  Rejected: "#ef4444",
};

function renderDecisionSector(props) {
  const { name } = props;

  return (
    <Sector
      {...props}
      fill={DECISION_COLORS[name]}
    />
  );
}

function renderDecisionLegend() {
  return (
    <div className="decision-legend">
      {Object.entries(DECISION_COLORS).map(([name, color]) => (
        <div className="legend-item" key={name}>
          <span
            className="legend-marker"
            style={{ backgroundColor: color }}
          />

          <span>{name}</span>
        </div>
      ))}
    </div>
  );
}

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [transactionsOverTime, setTransactionsOverTime] = useState([]);

  useEffect(() => {
    async function fetchSummary() {
      try {

        setLoading(true);
        setError("");

        const summaryData = await getDashboardSummary();
        const transactionsData = await getTransactionsOverTime();

        setSummary(summaryData);
        setTransactionsOverTime(transactionsData);
        
      } catch (error) {
        console.error("Failed to fetch dashboard summary:", error);

        setError("Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    }

    fetchSummary();
  }, []);

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  const decisionData = [
    { name: "Approved", value: summary.approved },
    { name: "Review", value: summary.review },
    { name: "Rejected", value: summary.rejected },
  ];



  return (
    <div>
      <h2>Dashboard</h2>

      <div className="dashboard-grid">
        <div className="kpi-card">
          <h3>Total Transactions</h3>
          <p>{summary.total_transactions}</p>
        </div>

        <div className="kpi-card">
          <h3>Approved</h3>
          <p>{summary.approved}</p>
        </div>

        <div className="kpi-card">
          <h3>Review</h3>
          <p>{summary.review}</p>
        </div>

        <div className="kpi-card">
          <h3>Rejected</h3>
          <p>{summary.rejected}</p>
        </div>
      </div>
      <div className="chart-card">
        <h3>Decision Distribution</h3>

        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={decisionData}
                dataKey="value"
                nameKey="name"
                innerRadius={70}
                outerRadius={100}
                shape={renderDecisionSector}
              >
              </Pie>

              <Tooltip />
              <Legend content={renderDecisionLegend}/>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="chart-card">
        <h3>Transactions Over Time</h3>

        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={transactionsOverTime}>
              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="date" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="count"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;