import React, { useEffect } from "react";
import { connect } from "react-redux";

//import "./hompage.styles.scss";
import { setCurrentUser } from "../../redux/actions/user.action";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const MainMerchant = ({ history, currentUser }) => {
  const signedIn = currentUser !== null && currentUser.type === "merchant";

  useEffect(() => {
    if (signedIn) {
      history.push(`/merchant/${currentUser.personId}`);
    }
  });

  return (
    <div>
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
    </div>
  );
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});

export default connect(mapStateToProps, { setCurrentUser })(MainMerchant);
