import React from "react";
import { Link } from "react-router-dom";

import "./header.styles.scss";

const Header = () => {
  return (
    <div className="header">
      <Link className="link-text" to="/">
        Facewallet
      </Link>
      <p>My Token = {window.token}</p>
    </div>
  );
};

export default Header;
