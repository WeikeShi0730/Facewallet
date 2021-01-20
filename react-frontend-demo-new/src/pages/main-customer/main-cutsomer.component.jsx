import React from "react";

//import "./hompage.styles.scss";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const MainCustomer = ({ history }) => {
  return (
    <div className="custom-button-container">
      <CustomButton
        onClick={() => {
          history.push("/user=customer/signin");
        }}
      >
        Sign In
      </CustomButton>
      <CustomButton
        onClick={() => {
          history.push("/customer/register");
        }}
      >
        Register
      </CustomButton>
    </div>
  );
};

export default MainCustomer;
