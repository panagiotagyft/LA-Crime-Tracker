import React, { createContext, useEffect, useState } from "react";
import axios from "axios";
import Cookies from "js-cookie";

export const AuthContext = createContext(null);

export const AuthContextProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(() => {
        const user = Cookies.get('user') ? JSON.parse(Cookies.get('user')) : null;
        if (user) {
            user.is_admin = Cookies.get('is_admin') === 'true';
        }
        return user;
    });

    const login = async (inputs) => {
        try {
            const response = await axios.post("https://127.0.0.1/api/token/", inputs, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
            if (response.status === 200 && response.data) {
                const user = response.data;
                setCurrentUser(user);
                Cookies.set('user', JSON.stringify(user));
                Cookies.set('is_admin', user.user.is_admin);
                return user.user;
            } else {
                throw new Error("Login Failed");
            }
        } catch (err) {
            console.error("Login failed", err);
            throw err;
        }
    };

    const logout = () => {
        Cookies.remove('user');
        Cookies.remove('is_admin');
    };

    useEffect(() => {
        if (currentUser) {
            Cookies.set('user', JSON.stringify(currentUser));
        } else {
            Cookies.remove('user');
        }
    }, [currentUser]);

    return (
        <AuthContext.Provider value={{ currentUser, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
