import React, { useRef, useCallback } from "react";
import { connect } from "react-redux";
import { useToasts } from 'react-toast-notifications'

import { setAmount } from "../../redux/actions/payment.action";
import { setIsLoading } from "../../redux/actions/loading.action";

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
<<<<<<< HEAD
        `/api/merchant/${currentUser.personId}/facepay`,
=======
        `${process.env.REACT_APP_BACKEND_URL}/api/merchant/${currentUser.personId}/facepay`,
>>>>>>> de518a04e2220ee5d65f1da6d822cbf0db356520
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
          alert(data.message + " " + data.person_id);
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
  isLoading: state.loading.isLoading,
  currentUser: state.user.currentUser,
});

export default connect(mapStateToProps, {
  setAmount,
  setIsLoading,
})(Payment);
