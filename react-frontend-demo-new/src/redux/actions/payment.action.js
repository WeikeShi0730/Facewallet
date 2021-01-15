import { SET_AMOUNT, SET_PHOTO, SET_LOADING } from "../actions/types";

export const setAmount = (price) => (dispatch) => {
  dispatch({
    type: SET_AMOUNT,
    payload: price,
  });
};

export const setIsLoading = (isLoading) => (dispatch) => {
  dispatch({
    type: SET_LOADING,
    payload: isLoading,
  });
};

export const setPhoto = (photo) => (dispatch) => {
  dispatch({
    type: SET_PHOTO,
    payload: photo,
  });
};
