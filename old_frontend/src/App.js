import React from 'react';
import { CssBaseline,
ThemeProvider } from '@mui/material';
import QuasarQuery from "./Containers/QuasarQuery/QuasarQuery";
import NotFound from "./Containers/NotFound/NotFound"
import { theme} from "./utils/theme";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import { ROUTE_PATHS } from "./routes/paths";
import "./App.css"

// import { Amplify } from "aws-amplify";
// import awsExports from "./aws-exports";
// import { Authenticator } from "@aws-amplify/ui-react";
// Amplify.configure({
//   Auth: {
//     region: awsExports.REGION,
//     userPoolId: awsExports.USER_POOL_ID,
//     userPoolWebClientId: awsExports.USER_POOL_APP_CLIENT_ID
//   }
// });

export default function MyApp() {
  return (
    <>
      <CssBaseline />
      <ThemeProvider theme = {theme}>
        <BrowserRouter>
         <Routes>
            <Route path = {ROUTE_PATHS.home} element = {<QuasarQuery/>} />
            <Route path = "*" element = {<NotFound/>} /> 
         </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </>
  );
}
