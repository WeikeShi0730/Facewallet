import React from "react";

import "./form-input.styles.scss";

const FormInput = ({ handleChange, label, value, ...otherProps }) => (
  <div className="group">
    <input
      className="form-input"
      onChange={handleChange}
      label={label}
      value={value}
      {...otherProps}
    />
    {/*
      Make shrinkable label form input 
    */}
    {label ? (
      <label className={`${value ? "shrink" : ""} form-input-label`}>
        {label}
      </label>
    ) : null}
  </div>
);

export default FormInput;
