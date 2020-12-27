import React from "react";
import { withRouter } from "react-router-dom";

import "./hompage.styles.scss";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const Homepage = ({ history }) => {
  return (
    <div className="custom-button-container">
      <CustomButton
        onClick={() => {
          history.push("/register");
        }}
      >
        Register
      </CustomButton>
      <CustomButton
        onClick={() => {
          history.push("/payment");
        }}
      >
        FacePay
      </CustomButton>
    </div>
  );
};

export default withRouter(Homepage);
