import { SET_CURRENT_MERCHANT } from "../actions/types";

const initialState = {
  currentMerchant: {
    id: "",
    type: "",
  },
};

export default function (state = initialState, action) {
  switch (action.type) {
    case SET_CURRENT_MERCHANT:
      return {
        ...state,
        currentMerchant: action.payload,
      };
    default:
      return state;
  }
}
