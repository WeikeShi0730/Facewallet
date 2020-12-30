import { combineReducers } from "redux";

import registerReducer from "./reducers/register.reducer";

const rootReducer = combineReducers({
  register: registerReducer,
});

export default rootReducer;
