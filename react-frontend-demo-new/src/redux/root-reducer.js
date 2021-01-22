import { combineReducers } from "redux";

import registerReducer from "./reducers/register.reducer";
import paymentReducer from "./reducers/payment.reducer";
import userReducer from "./reducers/user.reducer";

const rootReducer = combineReducers({
  register: registerReducer,
  payment: paymentReducer,
  user: userReducer,
});

export default rootReducer;
