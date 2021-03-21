import React from "react";
import { connect } from "react-redux";

//import "./hompage.styles.scss";

const ProfileCustomer = ({ currentUser }) => {
  const signedIn = currentUser !== null && currentUser.type === "customer";

  const transactions = currentUser.Transactions.map((transaction) => ({
    shop: transaction.Merchant.shop_name,
    amount: transaction.amount,
    time: transaction.data_time,
  }));

  return (
    <div>{signedIn ? <div>{currentUser.personId}</div> : <div></div>}</div>
  );
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps)(ProfileCustomer);
