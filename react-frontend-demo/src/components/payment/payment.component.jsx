import React from "react";
import { connect } from "react-redux";

import { setAmount } from "../../redux/actions/payment.action";
import { setIsLoading } from "../../redux/actions/register.action";

import "./payment.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import CustomButton from "../custom-buttom/custom-button.component";
import FormInput from "../form-input/form-input.component";

function Payment({ amount, isLoading, setAmount, setIsLoading }) {
  const handleChange = (event) => {
    const { value } = event.target;
    setAmount(value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (amount !== "") {
      setIsLoading(true);
      const response = await fetch(`/payment`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ amount: amount }),
      });
      console.log(JSON.stringify({ amount: amount }));

      setIsLoading(false);
      console.log(response);
      if (response.ok) {
        console.log("payment success!");
      }
    }
  };

  return (
    <div className={`${isLoading ? "isLoading" : "notLoading"}`}>
      <div className="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
      <div className="group">
        <WebcamWindow />
        <form onSubmit={handleSubmit}>
          <FormInput
            name="total"
            type="number"
            handleChange={handleChange}
            value={amount}
            label="Total"
            required
          />
          <CustomButton type="submit">Confirm</CustomButton>
        </form>
      </div>
    </div>
  );
}

const mapStateToProps = (state) => ({
  amount: state.payment.price,
  isLoading: state.register.isLoading,
});

export default connect(mapStateToProps, {
  setAmount,
  setIsLoading,
})(Payment);
