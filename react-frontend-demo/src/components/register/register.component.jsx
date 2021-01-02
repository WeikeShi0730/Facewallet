import React, { useState, useCallback, useEffect, useRef } from "react";
import { connect } from "react-redux";

import {
  setInfo,
  setButton,
  setStep,
  setPhoto,
  setIsLoading,
} from "../../redux/actions/register.action";

import "./register.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";
//import WithSpinner from "../with-spinner/with-spinner.component";

const Register = ({
  registerInfo,
  photoButton,
  step,
  photo,
  isLoading,
  setInfo,
  setButton,
  setStep,
  setPhoto,
  setIsLoading,
}) => {
  const [cardInfo, setCardInfo] = useState(registerInfo);

  const { name, cardNumber, cvv, expireDate } = cardInfo;

  const handleChange = (event) => {
    const { value, name } = event.target;
    setCardInfo({
      ...cardInfo,
      [name]: value,
    });
  };

  // webcam
  const webcamRef = useRef(null);
  const handleScreenshot = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setPhoto({ photo: imageSrc });
  }, [webcamRef, setPhoto]);

  useEffect(() => {
    async function getMessage() {
      const res = await fetch("/register", {
        method: "GET",
      });
      return res;
    }
    getMessage()
      .then((res) => res.json())
      .then((message) => console.log(message));
  }, [setStep]); //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  //const handleOnClick = async () => {};
  const handleSubmit = async (event) => {
    event.preventDefault();
    setInfo(cardInfo);
    setIsLoading(true);
    const response = await fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(cardInfo),
    });
    setIsLoading(false);
    //const filled = name && cardNumber && cvv && expireDate;
    if (response.ok) {
      setStep({
        ...step,
        info: true,
      });
      console.log("info regisration success!");
    }
  };

  const handleSendPhoto = async () => {
    if (photo.photo !== null) {
      console.log(JSON.stringify(photo));
      setIsLoading(true);
      const response = await fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(photo),
      });
      setIsLoading(false);
      if (response.ok) {
        setStep({
          ...step,
          photo: true,
        });
        console.log("photo regisration success!");
      }
    }
  };

  useEffect(() => {
    handleSendPhoto();
  }, [photo]);

  useEffect(() => {
    const { info, photo } = step;
    console.log(step);
    if (info) {
      setButton(false);
    }

    if (photo) {
      alert("Regisration is done!");
      setInfo({
        registerInfo: {
          name: "",
          cardNumber: "",
          cvv: "",
          expireDate: "",
        },
      });
    }
  }, [step, setButton, setInfo]);

  return (
    <div className={`${isLoading ? "isLoading" : "notLoading"}`}>
      <div className="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>

      <div className="register">
        <div className="form-submit">
          <form className="form" onSubmit={handleSubmit}>
            <FormInput
              name="cardNumber"
              type="text"
              handleChange={handleChange}
              value={cardNumber}
              label="Card Number"
              pattern="\d*"
              maxLength="16"
              required
            />

            <FormInput
              name="name"
              type="text"
              handleChange={handleChange}
              value={name}
              label="Name"
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
              required
            />

            <FormInput
              name="expireDate"
              type="date"
              handleChange={handleChange}
              value={expireDate}
              label="Expire Date"
              required
            />

            <CustomButton type="submit" disable={false}>
              Confirm
            </CustomButton>
          </form>
        </div>
        <div className="capture-window">
          <WebcamWindow className="webcam-window" ref={webcamRef} />
          <div className="capture-button">
            <CustomButton onClick={handleScreenshot} disable={photoButton}>
              Capture photo
            </CustomButton>
          </div>
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  photoButton: state.register.buttonDisabled,
  registerInfo: state.register.registerInfo,
  step: state.register.stepCheck,
  photo: state.register.image,
  isLoading: state.register.isLoading,
});

export default connect(mapStateToProps, {
  setInfo,
  setButton,
  setStep,
  setPhoto,
  setIsLoading,
})(Register);
