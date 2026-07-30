import Header from "./Header";
import Sidebar from "./Sidebar";

function Layout(){
  return(
    <div className="layout">
      <Header />
      <div className="content">
        <Sidebar />
        <main>
          <h2>Dashboard</h2>
          <p>Welcome to FraudScreen 👁️‍🗨️</p>
        </main>
      </div>
    </div>
  );
}

export default Layout;