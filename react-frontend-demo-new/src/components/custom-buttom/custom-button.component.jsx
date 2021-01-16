import React from "react";

import "./custom-button.styles.scss";

const CustomButton = ({ children, disable, ...props }) => (
  <button className="button" disabled={disable} {...props}>
    <div className={`${disable ? "disable" : ""}`}>{children}</div>
  </button>
);

export default CustomButton;
