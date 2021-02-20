import React from "react";
import { Switch, Route } from "react-router-dom";

import { GlobalStyle } from "./global.styles";

import Header from "./components/header/header.component";
import Homepage from "./pages/homepage/homepage.component";
import RegisterPage from "./pages/register/register.componnet";
import PaymentPage from "./pages/payment/payment.component";

function App() {
  return (
    <div>
      <GlobalStyle />
      <Header />
      <Switch>
        <Route exact path="/" component={Homepage} />
        <Route exact path="/register" component={RegisterPage} />
        <Route exact path="/payment" component={PaymentPage} />
      </Switch>
    </div>
  );
}

export default App;
