import React, { useRef, useCallback } from "react";
import { connect } from "react-redux";

import { setAmount } from "../../redux/actions/payment.action";
import { setIsLoading } from "../../redux/actions/register.action";

import "./payment.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import CustomButton from "../custom-buttom/custom-button.component";
import FormInput from "../form-input/form-input.component";

function Payment({ amount, isLoading, currentUser, setAmount, setIsLoading }) {
  const handleChange = (event) => {
    const { value } = event.target;
    setAmount(value);
  };

  // webcam
  const webcamRef = useRef(null);
  const handleScreenshot = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    return imageSrc;
  }, [webcamRef]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const imageSrc = handleScreenshot();
    if (imageSrc !== null && amount !== "") {
      setIsLoading(true);
      const response = await fetch(
        `/api/merchant/${currentUser.personId}/facepay`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ amount: amount, photo: imageSrc }),
        }
      );
      setIsLoading(false);
      if (response.ok) {
        try {
          const data = await response.json();
          if (data.message === "succeed") {
            console.log("payment success!", data);
            //write in to db
          }
          alert(data.message + " " + data.person_name);
        } catch (error) {
          console.log(error);
        }
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
        <WebcamWindow ref={webcamRef} />
        <form className="form" onSubmit={handleSubmit}>
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
  isLoading: state.payment.isLoading,
  currentUser: state.user.currentUser,
});

export default connect(mapStateToProps, {
  setAmount,
  setIsLoading,
})(Payment);
