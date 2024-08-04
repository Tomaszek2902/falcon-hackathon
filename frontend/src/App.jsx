import React from "react";
import { CssBaseline, Box, Toolbar } from "@mui/material";
import { Outlet } from "react-router-dom";
import Header from "./components/Header/Header";

const App = () => {
  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <Header />
      <Box component="main" sx={{ flexGrow: 1, p: 3, marginTop: "64px" }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
};

export default App;
