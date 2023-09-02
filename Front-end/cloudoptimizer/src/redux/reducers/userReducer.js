// userReducer.js
const initialState = {
    userID: null,
  };
  
  const userReducer = (state = initialState, action) => {
    switch (action.type) {
      case 'SET_USER_ID':
        return {
          ...state,
          userID: action.payload,
        };
      default:
        return state;
    }
  };
  
  export default userReducer;
  