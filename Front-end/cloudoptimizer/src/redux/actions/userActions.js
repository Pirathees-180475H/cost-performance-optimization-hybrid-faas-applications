export const setUser = (userID) => {
    return {
      type: 'SET_USER_ID',
      payload: userID,
    };
  };
  
  export const setCardCounts = (counts) => {
    return {
      type: 'SET_CARD_COUNTS',
      payload: counts,
    };
  };
  