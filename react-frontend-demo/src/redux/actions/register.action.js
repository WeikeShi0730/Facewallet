import { SET_INFO, SET_PHOTO_BUTTON, SET_STEP_CHECK } from "../actions/types";

export const setInfo = (info) => (dispatch) => {
  dispatch({
    type: SET_INFO,
    payload: info,
  });
};

export const setButton = (disabled) => (dispatch) => {
  dispatch({
    type: SET_PHOTO_BUTTON,
    payload: disabled,
  });
};

export const setStep = (step) => (dispatch) => {
  dispatch({
    type: SET_STEP_CHECK,
    payload: step,
  });
};
