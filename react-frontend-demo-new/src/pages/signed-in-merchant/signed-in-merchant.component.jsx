import React from "react";

//import "./hompage.styles.scss";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const SignedInMerchant = ({ history }) => {
  return (
    <div className="custom-button-container">
      <CustomButton
        onClick={() => {
          history.push("/merchant/signin");
        }}
      >
        Transaction
      </CustomButton>
      <CustomButton
        onClick={() => {
          history.push("/merchant/register");
        }}
      >
        Facepay
      </CustomButton>
    </div>
  );
};

export default SignedInMerchant;
