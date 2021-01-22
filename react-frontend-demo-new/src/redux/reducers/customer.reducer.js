import { SET_CURRENT_CUSTOMER } from "../actions/types";

const initialState = {
  currentCustomer: {
    id: "",
    type: "",
  },
};

export default function (state = initialState, action) {
  switch (action.type) {
    case SET_CURRENT_CUSTOMER:
      return {
        ...state,
        currentCustomer: action.payload,
      };
    default:
      return state;
  }
}
