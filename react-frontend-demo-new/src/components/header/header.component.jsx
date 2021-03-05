import React from "react";
import { Link } from "react-router-dom";

import "./header.styles.scss";

const Header = () => {
  return (
    <div className="header">
      <Link className="link-text" to="/">
        {`< Home`}
      </Link>
      <h3 className="title">FaceWallet</h3>
    </div>
  );
};

export default Header;
