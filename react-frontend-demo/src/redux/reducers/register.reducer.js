import {
  SET_INFO,
  SET_PHOTO_BUTTON,
  SET_STEP_CHECK,
  SET_PHOTO,
  SET_LOADING,
} from "../actions/types";

const initialState = {
  registerInfo: {
    name: "",
    cardNumber: "",
    cvv: "",
    expireDate: "",
  },

  buttonDisabled: true,

  stepCheck: {
    info: false,
    photo: false,
  },

  image: {
    photo: null,
  },

  isLoading: false,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case SET_INFO:
      return {
        ...state,
        registerInfo: action.payload,
      };
    case SET_PHOTO_BUTTON:
      return {
        ...state,
        buttonDisabled: action.payload,
      };

    case SET_STEP_CHECK:
      return {
        ...state,
        stepCheck: action.payload,
      };

    case SET_PHOTO:
      return {
        ...state,
        image: action.payload,
      };

    case SET_LOADING:
      return {
        ...state,
        isLoading: action.payload,
      };
    default:
      return state;
  }
}
