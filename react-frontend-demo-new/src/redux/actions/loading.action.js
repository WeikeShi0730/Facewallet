import { SET_LOADING } from "./types";

export const setIsLoading = (isLoading) => (dispatch) => {
  dispatch({
    type: SET_LOADING,
    payload: isLoading,
  });
};
