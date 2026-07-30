import { NavLink } from "react-router-dom";
function Sidebar() {
  return (
    <aside>
      <ul>
        <li>
          <NavLink
           to="/"
           className={({isActive}) =>
            isActive ? "active-link":""
          }
          >Dashboard</NavLink>
        </li>

        <li>
          <NavLink
           to="/transactions"
           className={({isActive}) =>
            isActive ? "active-link":""
          }
           >Transactions</NavLink>
        </li>

        <li>
          <NavLink
           to="/rules"
           className={({isActive}) =>
            isActive ? "active-link":""
          }
           >Rules</NavLink>
        </li>

        <li>
          <NavLink
           to="/fraud-evaluations"
           className={({isActive}) =>
            isActive ? "active-link":""
          }
          >Fraud Evaluations
          </NavLink>
        </li>
      </ul>
    </aside>
  );
}

export default Sidebar;