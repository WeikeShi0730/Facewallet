import { SET_AMOUNT } from "../actions/types";

const initialState = {
  price: "",
};

export default function (state = initialState, action) {
  switch (action.type) {
    case SET_AMOUNT:
      return {
        ...state,
        price: action.payload,
      };

    default:
      return state;
  }
}
