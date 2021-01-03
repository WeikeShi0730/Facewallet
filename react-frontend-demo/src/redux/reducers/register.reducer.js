import {
  SET_INFO,
  SET_PHOTO_BUTTON,
  SET_STEP_CHECK,
  SET_PHOTO,
  SET_LOADING,
  SET_PERSON_ID,
} from "../actions/types";

const initialState = {
  registerInfo: {
    first_name: "",
    last_name: "",
    phone_number: "",
    card_number: "",
    cvv: "",
    expire_date: "",
  },

  buttonDisabled: true,

  stepCheck: {
    info: false,
    photo: false,
  },

  image: null,

  isLoading: false,

  personId: null,
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

    case SET_PERSON_ID:
      return {
        ...state,
        personId: action.payload,
      };
    default:
      return state;
  }
}
