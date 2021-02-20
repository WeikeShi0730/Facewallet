import { SET_AMOUNT, SET_PHOTO, SET_LOADING } from "../actions/types";

const initialState = {
  price: "",
  image: null,
  isLoading: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case SET_AMOUNT:
      return {
        ...state,
        price: action.payload,
      };
    case SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
      };
    case SET_PHOTO:
      return {
        ...state,
        image: action.payload,
      };
    default:
      return state;
  }
}
