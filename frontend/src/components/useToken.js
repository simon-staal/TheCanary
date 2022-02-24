import { useState } from 'react';

export default function useToken() {
    const getToken = () => {
        return sessionStorage.getItem('token');
    };
    const [token, setToken] = useState(getToken());
    const saveToken = userToken => {
        console.log("Setting token: "+userToken)
        sessionStorage.setItem('token', userToken);
        setToken(userToken);
    };
    return {
        setToken: saveToken,
        token
    }

}