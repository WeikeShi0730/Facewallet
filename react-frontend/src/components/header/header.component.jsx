import React from "react";
import { Link } from "react-router-dom";

import "./header.styles.scss";

const Header = () => {
  return (
    <div className="header">
      <Link className="link-text" to="/">
        Facewallet
      </Link>
    </div>
  );
};

export default Header;
