import React from "react";
import { connect } from "react-redux";

//import "./hompage.styles.scss";
import { setCurrentUser } from "../../redux/actions/user.action";

import CustomButton from "../../components/custom-buttom/custom-button.component";

const MainCustomer = ({ history, currentUser, setCurrentUser }) => {
  const signedIn = currentUser !== null && currentUser.type === "customer";

  const logOut = () => {
    setCurrentUser({
      personId: "",
      type: "",
    });
  };

  return (
    <div>
      {signedIn ? (
        <div className="custom-button-container">
          <CustomButton
            onClick={() => {
              history.push(`/customer/${currentUser.personId}/profile`);
            }}
          >
            {currentUser.personId}
          </CustomButton>
          <CustomButton
            onClick={() => {
              logOut();
              history.push("/user=customer/signin");
            }}
          >
            Log Out
          </CustomButton>
        </div>
      ) : (
        <div className="custom-button-container">
          <CustomButton
            onClick={() => {
              history.push("/user=customer/signin");
            }}
          >
            Sign In
          </CustomButton>
          <CustomButton
            onClick={() => {
              history.push("/customer/register");
            }}
          >
            Register
          </CustomButton>
        </div>
      )}
    </div>
  );
};

const mapStateToProps = (state) => ({
  currentUser: state.user.currentUser,
});

export default connect(mapStateToProps, { setCurrentUser })(MainCustomer);
