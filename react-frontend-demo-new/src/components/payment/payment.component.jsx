import React, { useRef, useCallback, useEffect } from "react";
import { connect } from "react-redux";

import { setAmount, setPhoto } from "../../redux/actions/payment.action";
import { setIsLoading } from "../../redux/actions/register.action";

import "./payment.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import CustomButton from "../custom-buttom/custom-button.component";
import FormInput from "../form-input/form-input.component";

function Payment({
  amount,
  isLoading,
  photo,
  setAmount,
  setIsLoading,
  setPhoto,
}) {
  const handleChange = (event) => {
    const { value } = event.target;
    setAmount(value);
  };

  // webcam
  const webcamRef = useRef(null);
  const handleScreenshot = useCallback(
    (event) => {
      event.preventDefault();
      const imageSrc = webcamRef.current.getScreenshot();
      setPhoto(imageSrc);
    },
    [webcamRef, setPhoto]
  );

  useEffect(() => {
    handleSubmit(); // eslint-disable-next-line
  }, [photo]);

  const handleSubmit = async () => {
    if (photo !== null && amount !== "") {
      setIsLoading(true);
      const response = await fetch(`/payment`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ amount: amount, photo: photo }),
      });
      setIsLoading(false);
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
        <WebcamWindow ref={webcamRef} />
        <form className="form" onSubmit={handleScreenshot}>
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
  photo: state.payment.image,
});

export default connect(mapStateToProps, {
  setAmount,
  setIsLoading,
  setPhoto,
})(Payment);
