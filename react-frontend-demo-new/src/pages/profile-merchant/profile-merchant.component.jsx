import React, { useEffect, useState, useMemo } from "react";
import { connect } from "react-redux";
import { useToasts } from "react-toast-notifications";
import Table from "../../components/table/table.component";

import "./profile-merchant.styles.scss";

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
              cutomerName:
                instance.Customer.first_name +
                " " +
                instance.Customer.last_name,
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
        Header: "Customer Name",
        accessor: "cutomerName",
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
      {signedIn && transactions && transactions.length > 0 ? (
        <div>
          <h2>Hi {currentUser.firstName}!</h2>
          <Table columns={columns} data={data} />
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
