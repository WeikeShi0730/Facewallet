import React, { useCallback, useEffect, useRef } from "react";
import { connect } from "react-redux";
import { compose } from "redux";
import { withRouter } from "react-router-dom";

import {
  setInfo,
  setButton,
  setStep,
  setPhoto,
  setIsLoading,
  setPersonId,
} from "../../redux/actions/register.action";

import "./register.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";

const Register = ({
  registerInfo,
  photoButton,
  step,
  photo,
  isLoading,
  personId,
  setInfo,
  setButton,
  setStep,
  setPhoto,
  setIsLoading,
  setPersonId,
  history,
}) => {
  const {
    firstName,
    lastName,
    phoneNumber,
    cardNumber,
    cvv,
    expireDate,
  } = registerInfo;

  const handleChange = (event) => {
    const { value, name } = event.target;
    setInfo({
      ...registerInfo,
      [name]: value,
    });
  };

  // webcam
  const webcamRef = useRef(null);
  const handleScreenshot = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setPhoto(imageSrc);
  }, [webcamRef, setPhoto]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    history.push("/register/info");
    setIsLoading(true);
    const response = await fetch("/register/info", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(registerInfo),
    });
    console.log(registerInfo);
    setIsLoading(false);
    if (response.ok) {
      setStep({
        ...step,
        info: true,
      });
      const json = await response.json();
      const personId = json.person_id;
      setPersonId(personId);
      console.log("info regisration success!");
    }
  };

  const handleSendPhoto = async () => {
    if (photo !== null) {
      history.push(`/register/photo/${personId}`);
      setIsLoading(true);
      const response = await fetch(`/register/photo/${personId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ photo: photo }),
      });
      console.log(JSON.stringify({ photo: photo }));
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
    handleSendPhoto(); // eslint-disable-next-line
  }, [photo]);

  useEffect(() => {
    const { info, photo } = step;
    console.log(step);
    if (info) {
      setButton(false);
    }

    if (info && photo) {
      alert("Regisration is done!");
      setInfo({
        first_name: "",
        last_name: "",
        phone_number: "",
        card_number: "",
        cvv: "",
        expire_date: "",
      });
      setStep({ info: false, photo: false });
      setButton(true);
      setPhoto(null);
    }
  }, [step, setButton, setInfo, setStep, setPhoto]);

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
              name="first_name"
              type="text"
              handleChange={handleChange}
              value={firstName}
              label="First Name"
              required
            />
            <FormInput
              name="last_name"
              type="text"
              handleChange={handleChange}
              value={lastName}
              label="Last Name"
              required
            />

            <FormInput
              name="phone_number"
              type="text"
              handleChange={handleChange}
              value={phoneNumber}
              label="Phone Number"
              pattern="\d*"
              required
            />

            <FormInput
              name="card_number"
              type="text"
              handleChange={handleChange}
              value={cardNumber}
              label="Card Number"
              pattern="\d*"
              maxLength="16"
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
              name="expire_date"
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
  personId: state.register.personId,
});

export default compose(
  withRouter,
  connect(mapStateToProps, {
    setInfo,
    setButton,
    setStep,
    setPhoto,
    setIsLoading,
    setPersonId,
  })
)(Register);
