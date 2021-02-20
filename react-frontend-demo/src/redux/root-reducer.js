import { combineReducers } from "redux";

import registerReducer from "./reducers/register.reducer";
import paymentReducer from "./reducers/payment.reducer";

const rootReducer = combineReducers({
  register: registerReducer,
  payment: paymentReducer,
});

export default rootReducer;
