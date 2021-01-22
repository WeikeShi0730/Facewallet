import { SET_CURRENT_MERCHANT } from "./types";

export const setCurrentMerchant = (merchant) => (dispatch) => {
  dispatch({
    type: SET_CURRENT_MERCHANT,
    payload: merchant,
  });
};
