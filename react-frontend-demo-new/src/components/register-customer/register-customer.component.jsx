import React, { useCallback, useEffect, useRef, useState } from "react";
import { connect } from "react-redux";
import { compose } from "redux";
import { withRouter } from "react-router-dom";
import { useToasts } from "react-toast-notifications";

import {
  setButton,
  setStep,
  setPhoto,
} from "../../redux/actions/register.action";
import { setIsLoading } from "../../redux/actions/loading.action";
import { setCurrentUser } from "../../redux/actions/user.action";

import "./register-customer.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";

const Register = ({
  photoButton,
  step,
  photo,
  isLoading,
  setButton,
  setStep,
  setPhoto,
  setIsLoading,
  setCurrentUser,
  history,
}) => {
  const [registerInfo, setRegisterInfo] = useState({
    first_name: "",
    last_name: "",
    phone_number: "",
    email: "",
    password: "",
    confirm_password: "",
    card_number: "",
    cvv: "",
    expire_date: "",
  });
  const [personId, setPersonId] = useState();
  const [pwd, setPwd] = useState(false);
  const [match, setMatch] = useState(false);
  const { addToast } = useToasts();

  const {
    first_name,
    last_name,
    phone_number,
    email,
    password,
    confirm_password,
    card_number,
    cvv,
    expire_date,
  } = registerInfo;

  const handleChange = (event) => {
    const { value, name } = event.target;
    setRegisterInfo({
      ...registerInfo,
      [name]: value,
    });
    if (name === "password" || name === "confirm_password") {
      checkPassword(event);
      checkPasswordMatch();
    }
  };
  const checkPassword = (event) => {
    var pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;
    if (event.target.value.match(pattern)) {
      setPwd(true);
    } else {
      setPwd(false);
    }
  };
  const checkPasswordMatch = () => {
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    if (password !== undefined && password !== null && password !== "") {
      if (password === confirm_password) {
        setMatch(true);
      } else {
        setMatch(false);
      }
    } else {
      setMatch(false);
    }
  };

  // webcam
  const webcamRef = useRef(null);
  const handleScreenshot = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setPhoto(imageSrc);
  }, [webcamRef, setPhoto]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (match === false) {
      addToast("Passwords do not match", {
        appearance: "error",
        autoDismiss: true,
      });
      return;
    }
    if (pwd === false) {
      addToast("Passwords issue", {
        appearance: "error",
        autoDismiss: true,
      });
      return;
    }
    history.push("/customer/register/info");
    setIsLoading(true);
    let formData = new FormData();
    for (let field in registerInfo) {
      formData.append(field, registerInfo[field]);
    }
    const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/customer/register/info`, {
      method: "POST",
      body: formData,
    });
    setIsLoading(false);
    if (response.ok) {
      setStep({
        ...step,
        info: true,
      });
      const json = await response.json();
      try {
        const personId = json.person_id;
        setPersonId(personId);
        setCurrentUser({
          personId: personId,
          type: "customer",
        });
        addToast(json.message, {
          appearance: json.level,
          autoDismiss: true,
        });
      } catch (error) {
        console.log(error);
        addToast(error, {
          appearance: json.level,
          autoDismiss: true,
        });
      }
    }
  };

  const handleSendPhoto = async () => {
    if (photo !== null) {
      history.push(`/customer/register/photo/${personId}`);
      setIsLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/customer/register/photo/${personId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ photo: photo }),
      });
      setIsLoading(false);
      if (response.ok) {
        setStep({
          ...step,
          photo: true,
        });
        const json = await response.json();
        try {
          addToast(json.message, {
            appearance: "success",
            autoDismiss: true,
          });
        } catch (error) {
          console.log(error);
          addToast(error, {
            appearance: "error",
            autoDismiss: true,
          });
        }
      }
    }
  };

  useEffect(() => {
    setCurrentUser({
      personId: "",
      type: "",
    }); // eslint-disable-next-line
  }, []);

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
      history.push(`/customer/${personId}/profile`); //to profile page
      setRegisterInfo({
        first_name: "",
        last_name: "",
        phone_number: "",
        email: "",
        password: "",
        confirm_password: "",
        card_number: "",
        cvv: "",
        expire_date: "",
      });
      setStep({ info: false, photo: false });
      setButton(true);
      setPhoto(null);
    } // eslint-disable-next-line
  }, [step, setButton, setRegisterInfo, setStep, setPhoto]);

  return (
    <div className={`${isLoading ? "isLoading" : "notLoading"}`}>
      <div className="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>

      <div className="register-customer">
        <div className="form-submit">
          <form className="form" onSubmit={handleSubmit}>
            <FormInput
              name="first_name"
              type="text"
              handleChange={handleChange}
              value={first_name}
              label="First Name"
              required
            />
            <FormInput
              name="last_name"
              type="text"
              handleChange={handleChange}
              value={last_name}
              label="Last Name"
              required
            />

            <FormInput
              name="phone_number"
              type="text"
              handleChange={handleChange}
              value={phone_number}
              label="Phone Number"
              pattern="\d*"
              minLength="10"
              maxLength="11"
              required
            />
            <FormInput
              name="email"
              type="email"
              handleChange={handleChange}
              value={email}
              label="Email"
              required
            />
            <FormInput
              id="password"
              name="password"
              type="password"
              handleChange={handleChange}
              value={password}
              label="Password"
              minLength="8"
              maxLength="15"
              required
            />
            <div className="notice">
              <span className={`dot ${pwd ? "true" : ""}`}></span>
              <span>
                Should contain 8-15 characters, including lowercase letters,
                uppercase letters, digits and special symbols.
              </span>
            </div>
            <FormInput
              id="confirm_password"
              name="confirm_password"
              type="password"
              handleChange={handleChange}
              value={confirm_password}
              label="Confirm Password"
              minLength="8"
              maxLength="15"
              required
            />
            <div className="notice">
              <span className={`dot ${match ? "true" : ""}`}></span>
              <span>Password Match</span>
            </div>
            <FormInput
              name="card_number"
              type="text"
              handleChange={handleChange}
              value={card_number}
              label="Card Number"
              pattern="\d*"
              maxLength="16"
              minLength="16"
              required
            />

            <FormInput
              name="cvv"
              type="text"
              handleChange={handleChange}
              value={cvv}
              label="CVV (3 Digits)"
              pattern="\d*"
              minLength="3"
              maxLength="3"
              required
            />

            <FormInput
              name="expire_date"
              type="date"
              handleChange={handleChange}
              value={expire_date}
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
  step: state.register.stepCheck,
  photo: state.register.image,
  isLoading: state.loading.isLoading,
});

export default compose(
  withRouter,
  connect(mapStateToProps, {
    setButton,
    setStep,
    setPhoto,
    setIsLoading,
    setCurrentUser,
  })
)(Register);
