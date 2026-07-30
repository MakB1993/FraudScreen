import { BrowserRouter, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Rules from "./pages/Rules";
import FraudEvaluations from "./pages/FraudEvaluations";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="transactions" element={<Transactions />} />
          <Route path="rules" element={<Rules />} />
          <Route
            path="fraud-evaluations"
            element={<FraudEvaluations />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;