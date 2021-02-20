import { SET_CURRENT_USER } from "../actions/types";

const initialState = {
  currentUser: {
    personId: "",
    type: "",
  },
};

export default function (state = initialState, action) {
  switch (action.type) {
    case SET_CURRENT_USER:
      return {
        ...state,
        currentUser: action.payload,
      };
    default:
      return state;
  }
}
