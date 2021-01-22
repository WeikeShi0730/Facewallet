import React from "react";
import { connect } from "react-redux";

//import "./hompage.styles.scss";

const ProfileCustomer = ({ currentUser }) => {
  return <div>{currentUser.personId}</div>;
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps)(ProfileCustomer);
