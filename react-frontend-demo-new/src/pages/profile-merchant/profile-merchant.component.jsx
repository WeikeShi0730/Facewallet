import React from "react";
import { connect } from "react-redux";
//import "./hompage.styles.scss";

const ProfileMerchant = ({ currentUser }) => {
  const signedIn = currentUser !== null && currentUser.type === "merchant";
  return (
    <div>{signedIn ? <div>{currentUser.personId}</div> : <div></div>}</div>
  );
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps)(ProfileMerchant);
