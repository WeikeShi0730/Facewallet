import React, { useEffect, useState } from "react";
import { connect } from "react-redux";
import { compose } from "redux";
import { withRouter, useParams } from "react-router-dom";
import { useToasts } from "react-toast-notifications";

import { setCurrentUser } from "../../redux/actions/user.action";
import { setIsLoading } from "../../redux/actions/loading.action";

import "./sign-in.styles.scss";

import FormInput from "../form-input/form-input.component";
import CustomButton from "../custom-buttom/custom-button.component";

const SignIn = ({ isLoading, setIsLoading, setCurrentUser, history }) => {
  const [signInInfo, setSignInInfo] = useState({
    email: "",
    password: "",
  });
  const { addToast } = useToasts();

  const { email, password } = signInInfo;
  const handleChange = (event) => {
    const { value, name } = event.target;
    setSignInInfo({
      ...signInInfo,
      [name]: value,
    });
  };

  useEffect(() => {
    setCurrentUser({
      firstName: "",
      lastName: "",
      personId: "",
      type: "",
    }); // eslint-disable-next-line
  }, []);

  const { user } = useParams();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    let formData = new FormData();
    for (let field in signInInfo) {
      formData.append(field, signInInfo[field]);
    }
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}/api/${user}/signin`,
      {
        method: "POST",
        body: formData,
      }
    );
    setIsLoading(false);
    const json = await response.json();
    try {
      const personId = json.person_id;
      console.log(json);
      if (personId === undefined) {
        addToast(json.message, {
          appearance: json.level,
          autoDismiss: true,
        });
      } else {
        if (user === "customer") {
          setCurrentUser({
            firstName: json.first_name,
            lastName: json.last_name,
            personId: personId,
            type: "customer",
          });
        } else {
          setCurrentUser({
            firstName: json.first_name,
            lastName: json.last_name,
            personId: personId,
            type: "merchant",
          });
        }
        history.push(
          `/${user}/${personId}${user === "customer" ? "/profile" : ""}`
        );
      }
    } catch (error) {
      addToast(error, {
        appearance: "error",
        autoDismiss: true,
      });
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

      <div className="signin">
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
  isLoading: state.loading.isLoading,
});

export default compose(
  withRouter,
  connect(mapStateToProps, {
    setIsLoading,
    setCurrentUser,
  })
)(SignIn);
