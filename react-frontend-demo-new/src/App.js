import React from "react";
import { Switch, Route } from "react-router-dom";

import { GlobalStyle } from "./global.styles";

import Header from "./components/header/header.component";
import Homepage from "./pages/homepage/homepage.component";
import MainCustomer from "./pages/main-customer/main-cutsomer.component";
import MainMerchant from "./pages/main-merchant/main-merchant.component";
import Payment from "./pages/payment/payment.component";
import ProfileCustomer from "./pages/profile-customer/profile-customer.component";
import ProfileMerchant from "./pages/profile-merchant/profile-merchant.component";
import RegisterCustomer from "./pages/register-customer/register-customer.component";
import RegisterMerchant from "./pages/register-merchant/register-merchant.component";
import SignInPage from "./pages/sign-in/sign-in.component";
import SignedInMerchant from "./pages/signed-in-merchant/signed-in-merchant.component";

function App() {
  return (
    <div>
      <GlobalStyle />
      <Header />
      <Switch>
        <Route exact path="/" component={Homepage} />
        <Route exact path="/customer" component={MainCustomer} />
        <Route exact path="/merchant" component={MainMerchant} />
        <Route exact path="/customer/:customerId/profile" component={ProfileCustomer} />
        <Route
          exact
          path="/merchant/:merchantId/profile"
          component={ProfileMerchant}
        />
        <Route path="/customer/register" component={RegisterCustomer} />
        <Route exact path="/merchant/register" component={RegisterMerchant} />
        <Route exact path="/user=:user/signin" component={SignInPage} />
        <Route
          exact
          path="/merchant/:merchantId"
          component={SignedInMerchant}
        />
        <Route exact path="/merchant/:merchantId/payment" component={Payment} />
      </Switch>
    </div>
  );
}

export default App;
