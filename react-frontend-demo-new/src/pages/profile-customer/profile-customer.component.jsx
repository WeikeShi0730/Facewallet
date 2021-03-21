import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { useToasts } from "react-toast-notifications";

//import "./hompage.styles.scss";

const ProfileCustomer = ({ currentUser }) => {
  const { addToast } = useToasts();
  const { transactions, setTransactions } = useState();
  const signedIn = currentUser !== null && currentUser.type === "customer";

  useEffect(() => {
    handleSubmit();
  }, []);

  const handleSubmit = async (event) => {
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}/api/customer/${currentUser.personId}/profile`,
      {
        method: "GET",
      }
    );
    const json = await response.json();
    try {
      const personId = json.person_id;
      if (personId === undefined) {
        console.log(json);
        // addToast(json.message, {
        //   appearance: json.level,
        //   autoDismiss: true,
        // });
      } else {
        const transactions = currentUser.Transactions.map((transaction) => ({
          shop: transaction.Merchant.shop_name,
          amount: transaction.amount,
          time: transaction.data_time,
          balance: transaction.balance,
        }));
        console.log(transactions);
        setTransactions(transactions);
      }
    } catch (error) {
      // addToast(error, {
      //   appearance: "error",
      //   autoDismiss: true,
      // });
      console.log("User not found", error);
    }
  };

  return <div>{signedIn ? <div>{transactions}</div> : <div></div>}</div>;
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps)(ProfileCustomer);
