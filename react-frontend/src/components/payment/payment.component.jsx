import React, { useState } from "react";

import "./payment.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import CustomButton from "../custom-buttom/custom-button.component";
import FormInput from "../form-input/form-input.component";

function Payment() {
  const [price, setPrice] = useState({
    total: "",
  });

  const { total } = price;
  const handleSubmit = async (event) => {
    event.preventDefault();
  };

  const handleChange = (event) => {
    const { value, name } = event.target;
    setPrice({
      ...price,
      [name]: value,
    });
  };
  return (
    <div className="group">
      <WebcamWindow />
      <form onSubmit={handleSubmit}>
        <FormInput
          name="total"
          type="number"
          handleChange={handleChange}
          value={total}
          label="Total"
          required
        />
        <div className="button">
          <CustomButton type="submit">Confirm</CustomButton>
        </div>
      </form>
    </div>
  );
}

export default Payment;
