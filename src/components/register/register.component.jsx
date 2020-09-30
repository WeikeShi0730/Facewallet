import React, { useState } from "react";

import "./register.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";

function Register() {
  const [cardInfo, setCardInfo] = useState({
    name: "",
    cardNumber: "",
    cvv: "",
    expireDate: "",
  });

  const [disabled, setDisabled] = useState({
    disabled: false,
  });

  const { name, cardNumber, cvv, expireDate } = cardInfo;

  const handleSubmit = async (event) => {
    event.preventDefault();
  };

  const handleChange = (event) => {
    const { value, name } = event.target;
    setCardInfo({
      ...cardInfo,
      [name]: value,
    });
  };

  const handleDisabled = (event) => {
    setDisabled(!disabled);
  };

  return (
    <div className="register">
      <WebcamWindow />
      <form className={disabled ? "disabled" : ""} onSubmit={handleSubmit}>
        <FormInput
          name="cardNumber"
          type="text"
          handleChange={handleChange}
          value={cardNumber}
          label="Card Number"
          pattern="\d*"
          maxLength="16"
          disabled={disabled}
          required
        />

        <FormInput
          name="name"
          type="text"
          handleChange={handleChange}
          value={name}
          label="Name"
          disabled={disabled}
          required
        />

        <FormInput
          name="cvv"
          type="text"
          handleChange={handleChange}
          value={cvv}
          label="CVV (3 Digits)"
          pattern="\d*"
          maxLength="3"
          disabled={disabled}
          required
        />

        <FormInput
          name="expireDate"
          type="date"
          handleChange={handleChange}
          value={expireDate}
          label="Expire Date"
          disabled={disabled}
          required
        />

        <div className="button">
          <CustomButton type="submit">Confirm</CustomButton>
          <CustomButton onClick={handleDisabled} type="submit">
            pass
          </CustomButton>
        </div>
      </form>
    </div>
  );
}

export default Register;
