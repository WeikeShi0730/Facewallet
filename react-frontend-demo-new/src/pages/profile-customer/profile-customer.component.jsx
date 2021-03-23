import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { useToasts } from "react-toast-notifications";

//import "./hompage.styles.scss";

const ProfileCustomer = ({ currentUser }) => {
  const { addToast } = useToasts();
  const [transactions, setTransactions] = useState();
  const signedIn = currentUser !== null && currentUser.type === "customer";

  useEffect(() => {
    const handleSubmit = async () => {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/customer/${currentUser.personId}/profile`,
        {
          method: "GET",
        }
      );
      const json = await response.json();
      try {
        const customer = json.Customer;
        const transactions_json = json.Transaction;

        console.log(json);
        if (
          customer.id === undefined ||
          customer.id === null ||
          customer.id === ""
        ) {
          addToast(json.message, {
            appearance: json.level,
            autoDismiss: true,
          });
        } else if (customer.id === currentUser.personId) {
          const transactions_list = [];
          for (const transaction in transactions_json) {
            const instance = transactions_json[transaction];
            transactions_list.push({
              key: instance.trans_id,
              shopName: instance.Merchant.shop_name,
              amount: instance.amount,
              time: instance.date_time,
            });
          }
          setTransactions(transactions_list);
        }
      } catch (error) {
        addToast(error, {
          appearance: "error",
          autoDismiss: true,
        });
        console.log("User not found", error);
      }
    };
    handleSubmit(); // eslint-disable-next-line
  }, []);

  return (
    <div>
      {signedIn && transactions && transactions.length > 0 ? (
        <div>
          {transactions.map((transaction) => (
            <div key={transaction.key}>
              <span> {transaction.shopName}------</span>
              <span> {transaction.amount}------</span>
              <span> {transaction.time} </span>
            </div>
          ))}
        </div>
      ) : (
        <div>No records found</div>
      )}
    </div>
  );
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps)(ProfileCustomer);
