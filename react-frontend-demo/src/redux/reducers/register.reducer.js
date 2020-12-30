import { SET_INFO, SET_PHOTO_BUTTON, SET_STEP_CHECK } from "../actions/types";

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

    default:
      return state;
  }
}
