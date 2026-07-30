import { Outlet } from "react-router-dom";

import Header from "./Header";
import Sidebar from "./Sidebar";

function Layout() {
  return (
    <div className="layout">
      <Header />

      <div className="content">
        <div className="sidebar">
          <Sidebar />
        </div>

        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default Layout;