import React, { useState } from "react";
import { connect } from "react-redux";
import { compose } from "redux";
import { withRouter, useParams } from "react-router-dom";

import { setIsLoading, setPersonId } from "../../redux/actions/register.action";
import { setCurrentCustomer } from "../../redux/actions/customer.action";
import { setCurrentMerchant } from "../../redux/actions/merchant.action";
import { setCurrentUser } from "../../redux/actions/user.action";

import "./sign-in.styles.scss";

import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";

const SignIn = ({
  isLoading,
  setIsLoading,
  setPersonId,
  setCurrentUser,
  history,
}) => {
  const [signInInfo, setSignInInfo] = useState({
    email: "",
    password: "",
  });

  const { email, password } = signInInfo;
  const handleChange = (event) => {
    const { value, name } = event.target;
    setSignInInfo({
      ...signInInfo,
      [name]: value,
    });
  };

  const { user } = useParams();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let formData = new FormData();
    for (let field in signInInfo) {
      formData.append(field, signInInfo[field]);
    }
    const response = await fetch(`/api/${user}/signin`, {
      method: "POST",
      body: formData,
    });
    setIsLoading(false);
    const json = await response.json();
    try {
      const personId = json.person_id;
      if (personId === undefined) {
        alert(json.error);
      } else {
        setPersonId(personId);
        if (user === "customer") {
          setCurrentUser({
            personId: personId,
            type: "customer",
          });
        } else {
          setCurrentUser({
            personId: personId,
            type: "merchant",
          });
        }
        history.push(`/${user}/${personId}/profile`);
      }
    } catch (error) {
      console.log("User not found", error);
    }
  };

  return (
    <div className={`${isLoading ? "isLoading" : "notLoading"}`}>
      <div className="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>

      <div className="register">
        <div className="form-submit">
          <form className="form" onSubmit={handleSubmit}>
            <FormInput
              name="email"
              type="email"
              handleChange={handleChange}
              value={email}
              label="Email"
              required
            />
            <FormInput
              name="password"
              type="password"
              handleChange={handleChange}
              value={password}
              label="Password"
              required
            />

            <CustomButton type="submit" disable={false}>
              Confirm
            </CustomButton>
          </form>
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  isLoading: state.register.isLoading,
});

export default compose(
  withRouter,
  connect(mapStateToProps, {
    setIsLoading,
    setPersonId,
    setCurrentCustomer,
    setCurrentMerchant,
    setCurrentUser,
  })
)(SignIn);
