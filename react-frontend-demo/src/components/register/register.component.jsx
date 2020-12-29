import React, { useState, useCallback, useEffect, useRef } from "react";

import "./register.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";
import WithSpinner from "../with-spinner/with-spinner.component";

const Register = (props) => {
  const [photo, setPhoto] = useState({
    photo: null,
  });
  const [cardInfo, setCardInfo] = useState({
    name: "",
    cardNumber: "",
    cvv: "",
    expireDate: "",
  });

  // const { setIsLoading } = props;
  // useEffect(() => {
  //   setIsLoading(false);
  // });

  const [disable, setDisable] = useState(true);

  const [register, setRegister] = useState({
    info: false,
    photo: false,
  });

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
    handleSendPhoto();
  }, [webcamRef, photo]);

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
  }, [register]);

  //const handleOnClick = async () => {};
  const handleSubmit = async (event) => {
    event.preventDefault();
    //setIsLoading(true);
    const response = await fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(cardInfo),
    });
    //setIsLoading(false);
    const filled = name && cardNumber && cvv && expireDate;
    if (response.ok && filled) {
      setRegister({
        ...register,
        info: true,
      });
      console.log("info regisration success!");
    }
  };

  const handleSendPhoto = async () => {
    //setIsLoading(true);
    const response = await fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(photo),
    });
    //setIsLoading(false);
    if (response.ok) {
      setRegister({
        ...register,
        photo: true,
      });
      console.log("photo regisration success!");
    }
  };

  useEffect(() => {
    const { info, photo } = register;
    if (info) {
      setDisable(false);
    }

    if (photo) {
      alert("Regisration is done!");
      setCardInfo({
        name: "",
        cardNumber: "",
        cvv: "",
        expireDate: "",
      });
    }
  }, [register]);

  return (
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
          <CustomButton onClick={handleScreenshot} disable={disable}>
            Capture photo
          </CustomButton>
        </div>
      </div>
    </div>
  );
};

//export default WithSpinner(Register);
export default Register;
