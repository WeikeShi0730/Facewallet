import { SET_CURRENT_CUSTOMER } from "./types";

export const setCurrentCustomer = (customer) => (dispatch) => {
  dispatch({
    type: SET_CURRENT_CUSTOMER,
    payload: customer,
  });
};
