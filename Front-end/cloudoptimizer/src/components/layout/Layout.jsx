import React, { useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import ThemeAction from '../../redux/actions/ThemeAction';
import LoginLayout from './loginLayout';
import DefaultLayout from './defaultLayout';

const Layout = () => {
    const themeReducer = useSelector((state) => state.ThemeReducer);
    const dispatch = useDispatch();

    useEffect(() => {
        const themeClass = localStorage.getItem('themeMode', 'theme-mode-light');
        const colorClass = localStorage.getItem('colorMode', 'theme-mode-light');

        dispatch(ThemeAction.setMode(themeClass));
        dispatch(ThemeAction.setColor(colorClass));
    }, [dispatch]);

    return (
        <BrowserRouter>
            <Switch>
                <Route exact path={['/', '/login', '/signup']}>
                    <LoginLayout themeMode={themeReducer.mode} colorMode={themeReducer.color} />
                </Route>
                <Route>
                    <DefaultLayout themeMode={themeReducer.mode} colorMode={themeReducer.color} />
                </Route>
            </Switch>
        </BrowserRouter>
    );
};

export default Layout;
