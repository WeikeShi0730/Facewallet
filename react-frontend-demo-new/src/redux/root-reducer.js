import { combineReducers } from "redux";

import registerReducer from "./reducers/register.reducer";
import paymentReducer from "./reducers/payment.reducer";
import userReducer from "./reducers/user.reducer";
import loadingReducer from "./reducers/loading.reducer";

const rootReducer = combineReducers({
  register: registerReducer,
  payment: paymentReducer,
  loading: loadingReducer,
  user: userReducer,
});

export default rootReducer;
