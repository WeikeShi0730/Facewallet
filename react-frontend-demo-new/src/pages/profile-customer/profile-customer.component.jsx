import React, { useEffect, useState, useMemo } from "react";
import { connect } from "react-redux";
import { useToasts } from "react-toast-notifications";
import Table from "../../components/table/table.component";

import "./profile-customer.styles.scss";

const ProfileCustomer = ({ currentUser }) => {
  const { addToast } = useToasts();
  const [transactions, setTransactions] = useState([]);
  const [balance, setBalance] = useState([]);

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
          console.log(currentUser);
          setBalance(customer.balance);
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

  const data = useMemo(() => transactions, [transactions]);
  const columns = useMemo(
    () => [
      {
        Header: "Transaction ID#",
        accessor: "key",
      },
      {
        Header: "Shop",
        accessor: "shopName",
      },
      {
        Header: "Date",
        accessor: "time",
      },
      {
        Header: "Amount (CAD)",
        accessor: "amount",
        Footer: (info) => {
          // Only calculate total visits if rows change
          const total = React.useMemo(
            () => info.rows.reduce((sum, row) => row.values.amount + sum, 0),
            [info.rows]
          );
          return <div>Total: {total}</div>;
        },
      },
    ],
    []
  );

  return (
    <div>
      <h2>Hi {currentUser.firstName}!</h2>
      {signedIn && transactions && transactions.length > 0 ? (
        <div>
          <h4>Current Balance: ${balance}</h4>
          <Table columns={columns} data={data} />
        </div>
      ) : (
        <h4>No records found</h4>
      )}
    </div>
  );
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});
export default connect(mapStateToProps)(ProfileCustomer);
