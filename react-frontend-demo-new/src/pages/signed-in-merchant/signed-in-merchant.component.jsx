import React from "react";
import { connect } from "react-redux";

//import "./hompage.styles.scss";
import { setCurrentUser } from "../../redux/actions/user.action";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const SignedInMerchant = ({ history, currentUser, setCurrentUser }) => {
  const logOut = () => {
    setCurrentUser({
      personId: "",
      type: "",
    });
  };
  return (
    <div className="custom-button-container">
      <CustomButton
        onClick={() => {
          history.push(`/merchant/${currentUser.personId}/profile`);
        }}
      >
        Transaction
      </CustomButton>
      <CustomButton
        onClick={() => {
          history.push(`/merchant/${currentUser.personId}/payment`);
        }}
      >
        Facepay
      </CustomButton>
      <CustomButton
        onClick={() => {
          logOut();
          history.push(`/merchant`);
        }}
      >
        Log Out
      </CustomButton>
    </div>
  );
};
const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps, { setCurrentUser })(SignedInMerchant);
