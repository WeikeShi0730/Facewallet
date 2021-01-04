import { SET_AMOUNT } from "../actions/types";

export const setAmount = (price) => (dispatch) => {
  dispatch({
    type: SET_AMOUNT,
    payload: price,
  });
};
