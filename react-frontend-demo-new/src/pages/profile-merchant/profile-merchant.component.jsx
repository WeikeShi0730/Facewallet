import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { useToasts } from "react-toast-notifications";

//import "./hompage.styles.scss";

const ProfileMerchant = ({ currentUser }) => {
  const { addToast } = useToasts();
  const [transactions, setTransactions] = useState();
  const signedIn = currentUser !== null && currentUser.type === "merchant";

  useEffect(() => {
    const handleSubmit = async () => {
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/merchant/${currentUser.personId}/profile`,
        {
          method: "GET",
        }
      );
      const json = await response.json();
      try {
        const merchant = json.Merchant;
        const transactions_json = json.Transaction;
        console.log(json)
        if (
          merchant.id === undefined ||
          merchant.id === null ||
          merchant.id === ""
        ) {
          addToast(json.message, {
            appearance: json.level,
            autoDismiss: true,
          });
        } else if (merchant.id === currentUser.personId) {
          const transactions_list = [];
          for (const transaction in transactions_json) {
            const instance = transactions_json[transaction];
            transactions_list.push({
              key: instance.trans_id,
              cutomerName: instance.Customer.first_name + " " + instance.Customer.last_name,
              cardNumber: instance.Customer.card_number,
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
              <span> {transaction.cutomerName}------</span>
              <span> {transaction.cardNumber}------</span>
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
export default connect(mapStateToProps)(ProfileMerchant);
