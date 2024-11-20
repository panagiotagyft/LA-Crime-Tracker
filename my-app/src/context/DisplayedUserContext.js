import React, { createContext, useState } from 'react';

export const DisplayedUserContext = createContext();

export const DisplayedUserProvider = ({ children }) => {
  const [displayedUser, setDisplayedUser] = useState(null);

  return (
    <DisplayedUserContext.Provider value={{ displayedUser, setDisplayedUser }}>
      {children}
    </DisplayedUserContext.Provider>
  );
};
