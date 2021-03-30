import React, { useRef, useState, useCallback } from "react";
import { connect } from "react-redux";
import { useToasts } from "react-toast-notifications";
import NumPad from "react-numpad";

import { setAmount } from "../../redux/actions/payment.action";
import { setIsLoading } from "../../redux/actions/loading.action";

import "./payment.styles.scss";

import WebcamWindow from "../camera-window/camera-window.component";
import CustomButton from "../custom-buttom/custom-button.component";
import FormInput from "../form-input/form-input.component";
import CustomModal from "../modal/modal.component";

function Payment({ amount, isLoading, currentUser, setAmount, setIsLoading }) {
  const { addToast } = useToasts();
  const [checkmark, setCheckmark] = useState(0);
  const [show, setShow] = useState(false);
  const [phoneNumber, setPhoneNumber] = useState();
  const [image, setImage] = useState();

  const handleChange = (event) => {
    const { name, value } = event.target;
    if (name === "phone_number") {
      setPhoneNumber(value);
    } else if (name === "total") {
      setAmount(value);
    }
  };

  // webcam
  const webcamRef = useRef(null);
  const handleScreenshot = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
    return imageSrc;
  }, [webcamRef]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const imageSrc = handleScreenshot();
    if (imageSrc !== null && amount !== "") {
      setIsLoading(true);
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/merchant/${currentUser.personId}/facepay`,
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
        const json = await response.json();
        try {
          if (json.message === "succeed") {
            console.log("payment success!", json);
            // Checkmark animation timeout
            setCheckmark(1);
            setTimeout(() => {
              setCheckmark(0);
            }, 2500);
            setAmount(0);
          } else if (json.sec_verification === "True") {
            console.log("need seocndary verification");
            setShow(true);
          }
          addToast(json.message, {
            appearance: json.level,
            autoDismiss: true,
          });
          return;
        } catch (error) {
          console.log(error);
          addToast(error.message, {
            appearance: json.level,
            autoDismiss: true,
          });
        }
      }
    }
  };

  const handleSubmitSecondary = async (event) => {
    event.preventDefault();
    if (
      phoneNumber !== undefined &&
      phoneNumber !== null &&
      phoneNumber !== ""
    ) {
      setIsLoading(true);

      console.log(amount);
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/merchant/${currentUser.personId}/facepay/verification`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: amount,
            photo: image,
            phone_number: phoneNumber,
          }),
        }
      );
      setIsLoading(false);
      if (response.ok) {
        const json = await response.json();
        try {
          if (json.message === "succeed") {
            console.log("payment success!", json);
            // Checkmark animation timeout
            setCheckmark(1);
            setTimeout(() => {
              setCheckmark(0);
            }, 2500);
            setShow(false);
          }
          addToast(json.message, {
            appearance: json.level,
            autoDismiss: true,
          });
        } catch (error) {
          console.log(error);
          addToast(error.message, {
            appearance: json.level,
            autoDismiss: true,
          });
        }
      }
      setPhoneNumber("");
      setAmount(0);
    } else {
      addToast("Please input your phone number", {
        appearance: "warning",
        autoDismiss: true,
      });
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

      <CustomModal
        title="Secondary Verification"
        onSubmit={handleSubmitSecondary}
        onClose={() => setShow(false)}
        show={show}
      >
        <label>Please Enter Phone Number</label>
        <form className="form">
          <FormInput
            name="phone_number"
            type="text"
            handleChange={handleChange}
            value={phoneNumber}
            label="Phone Number"
            pattern="\d*"
            minLength="10"
            maxLength="11"
            required
          />
        </form>
      </CustomModal>

      <div className="group">
        <div className={`${checkmark === 1 ? "mark" : ""}`}>
          <svg
            className={`${checkmark === 1 ? "checkmark" : "uncheckmark"}`}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 52 52"
          >
            <circle
              className={`${checkmark === 1 ? "checkmark__circle" : ""}`}
              cx="50%"
              cy="50%"
              r="25"
              fill="none"
            />
            <path
              className={`${checkmark === 1 ? "checkmark__check" : ""}`}
              fill="none"
              d="M14.1 27.2l7.1 7.2 16.7-16.8"
            />
          </svg>
        </div>
        <WebcamWindow ref={webcamRef} />

        <form className="form" onSubmit={handleSubmit}>
          <NumPad.Number
            decimal={2}
            negative={false}
            onChange={(value) => setAmount(Number(value))}
          >
            <FormInput
              handleChange={handleChange}
              name="total"
              type="number"
              value={amount}
              label="Total"
              required
            />
          </NumPad.Number>
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
