import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { compose } from "redux";
import { withRouter } from "react-router-dom";

import { setIsLoading } from "../../redux/actions/loading.action";

import "./register-merchant.styles.scss";

import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";
import { setCurrentUser } from "../../redux/actions/user.action";

const Register = ({ isLoading, setIsLoading, setCurrentUser, history }) => {
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

  const [pwd, setPwd] = useState(false);
  const [match, setMatch] = useState(false);

  const handleChange = (event) => {
    const { value, name } = event.target;
    setRegisterInfo({
      ...registerInfo,
      [name]: value,
    });
    if (name === "password" || name === "confirm_password") {
      checkPassword(event);
      checkPasswordMatch();
    }
  };
  const checkPassword = (event) => {
    var pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;
    if (event.target.value.match(pattern)) {
      setPwd(true);
    } else {
      setPwd(false);
    }
  };
  const checkPasswordMatch = () => {
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;
    if (password !== undefined && password !== null && password !== "") {
      if (password === confirm_password) {
        setMatch(true);
      } else {
        setMatch(false);
      }
    } else {
      setMatch(false);
    }
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let formData = new FormData();
    for (let field in registerInfo) {
      formData.append(field, registerInfo[field]);
    }
    const response = await fetch("/api/merchant/register", {
      method: "POST",
      body: formData,
    });
    console.log(registerInfo);
    setIsLoading(false);
    if (response.ok) {
      const json = await response.json();
      try {
        const personId = json.person_id;
        setCurrentUser({
          personId: personId,
          type: "merchant",
        });
        console.log("info regisration success!");
        history.push(`/merchant/${personId}`);
      } catch (error) {
        console.log(error);
      }
    }
  };

  useEffect(() => {
    setCurrentUser({
      personId: "",
      type: "",
    }); // eslint-disable-next-line
  }, []);

  return (
    <div className={`${isLoading ? "isLoading" : "notLoading"}`}>
      <div className="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>

      <div className="register-merchant">
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
              id="password"
              name="password"
              type="password"
              handleChange={handleChange}
              value={password}
              label="Password"
              minLength="8"
              maxLength="15"
              required
            />
            <div className="notice">
              <span className={`dot ${pwd ? "true" : ""}`}></span>
              <span>
                Should contain 8-15 characters, including lowercase letters,
                uppercase letters, digits and special symbols.
              </span>
            </div>
            <FormInput
              id="confirm_password"
              name="confirm_password"
              type="password"
              handleChange={handleChange}
              value={confirm_password}
              label="Confirm Password"
              minLength="8"
              maxLength="15"
              required
            />
            <div className="notice">
              <span className={`dot ${match ? "true" : ""}`}></span>
              <span>Password Match</span>
            </div>

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
  isLoading: state.loading.isLoading,
  personId: state.register.personId,
});

export default compose(
  withRouter,
  connect(mapStateToProps, {
    setIsLoading,
    setCurrentUser,
  })
)(Register);
