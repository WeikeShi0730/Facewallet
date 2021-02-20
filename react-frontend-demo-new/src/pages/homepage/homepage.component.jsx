import React from "react";
import { withRouter } from "react-router-dom";

import "./hompage.styles.scss";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const Homepage = ({ history }) => {
  return (
    <div className="custom-button-container">
      <CustomButton
        onClick={() => {
          history.push("/customer");
        }}
      >
        Customer
      </CustomButton>
      <CustomButton
        onClick={() => {
          history.push("/merchant");
        }}
      >
        Merchant
      </CustomButton>
    </div>
  );
};

export default withRouter(Homepage);
