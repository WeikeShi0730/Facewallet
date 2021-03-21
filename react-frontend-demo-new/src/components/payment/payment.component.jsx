import React, { useRef, useState, useCallback } from "react";
import { connect } from "react-redux";
import { useToasts } from "react-toast-notifications";

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
          } else if (json.message === "Secondary verification needed") {
            console.log("need seocndary verification");
            setShow(true);
          }
          addToast(json.message + " " + json.person_id, {
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
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/merchant/${currentUser.personId}/facepay/verification`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ phone_number: phoneNumber }),
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
          addToast(json.message + " " + json.person_id, {
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

  return (
    <div className={`${isLoading ? "isLoading" : "notLoading"}`}>
      <div className="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>

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

      <CustomModal
        title="Secondary Verification"
        onClose={() => setShow(false)}
        show={show}
      >
        <label>Please Enter Phone Number</label>
        <FormInput
          name="phone_number"
          type="text"
          handleChange={handleSubmitSecondary}
          value={phoneNumber}
          label="Phone Number"
          pattern="\d*"
          minLength="10"
          maxLength="11"
          required
        />
      </CustomModal>

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
