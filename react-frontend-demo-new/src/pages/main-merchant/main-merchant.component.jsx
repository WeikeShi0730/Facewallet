import React from "react";

//import "./hompage.styles.scss";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const MainMerchant = ({ history }) => {
  return (
    <div className="custom-button-container">
      <CustomButton
        onClick={() => {
          history.push("/user=merchant/signin");
        }}
      >
        Sign In
      </CustomButton>
      <CustomButton
        onClick={() => {
          history.push("/merchant/register");
        }}
      >
        Register
      </CustomButton>
    </div>
  );
};

export default MainMerchant;
