import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Login from './pages/login/Login';
import Register from './pages/register/Register';
import Home from './pages/home/Home';
import Queries from './pages/queries/Queries';
import Insert from './pages/insert/Insert';
import Updates from './pages/updates/Updates';

const router = createBrowserRouter([
  { path: "/", element: <Login /> },
  { path: "/login", element: <Login /> },
  { path: "/register", element: <Register /> },
  { path: "/home", element: <Home /> },
  { path: "/queries", element: <Queries /> },
  { path: "/insert", element: <Insert /> },
  { path: "/updates", element: <Updates /> },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
