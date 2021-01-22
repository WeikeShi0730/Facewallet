import React, { useEffect } from "react";
import { connect } from "react-redux";

//import "./hompage.styles.scss";

const ProfileCustomer = ({ currentUser }) => {

  


  return <div>{currentUser}</div>;
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps)(ProfileCustomer);
