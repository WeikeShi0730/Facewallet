import React from "react";
import { Link } from "react-router-dom";

import logo from "../../assets/logo.png";
import "./header.styles.scss";

const Header = () => {
  return (
    <div className="header">
      <Link className="link-text" to="/">
        {`< Home`}
      </Link>
      <div className="group">
        <img src={logo} className="logo" alt="Logo" />
        <h3 className="title">FaceWallet</h3>
      </div>
    </div>
  );
};

export default Header;
