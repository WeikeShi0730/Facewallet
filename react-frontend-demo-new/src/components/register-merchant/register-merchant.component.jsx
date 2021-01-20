import React, { useState } from "react";
import { connect } from "react-redux";
import { compose } from "redux";
import { withRouter } from "react-router-dom";

import { setIsLoading, setPersonId } from "../../redux/actions/register.action";

//import "./register-merchant.styles.scss";

import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";

const Register = ({
  isLoading,
  personId,
  setIsLoading,
  setPersonId,
  history,
}) => {
  const [registerInfo, setRegisterInfo] = useState({
    first_name: "",
    last_name: "",
    shop_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });
  const {
    first_name,
    last_name,
    shop_name,
    email,
    password,
    confirm_password,
  } = registerInfo;

  const handleChange = (event) => {
    const { value, name } = event.target;
    setRegisterInfo({
      ...registerInfo,
      [name]: value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let formData = new FormData();
    for (let field in registerInfo) {
      formData.append(field, registerInfo[field]);
    }
    const response = await fetch("api/merchant/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: formData,
    });
    console.log(registerInfo);
    setIsLoading(false);
    if (response.ok) {
      const json = await response.json();
      const personId = json.person_id;
      setPersonId(personId);
      console.log("info regisration success!");
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
              name="first_name"
              type="text"
              handleChange={handleChange}
              value={first_name}
              label="First Name"
              required
            />
            <FormInput
              name="last_name"
              type="text"
              handleChange={handleChange}
              value={last_name}
              label="Last Name"
              required
            />

            <FormInput
              name="shop_name"
              type="text"
              handleChange={handleChange}
              value={shop_name}
              label="Shop Name"
              required
            />

            <FormInput
              name="email"
              type="text"
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

            <FormInput
              name="confirm_password"
              type="password"
              handleChange={handleChange}
              value={confirm_password}
              label="Confirm Password"
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
  personId: state.register.personId,
});

export default compose(
  withRouter,
  connect(mapStateToProps, {
    setIsLoading,
    setPersonId,
  })
)(Register);
