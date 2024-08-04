import React from "react";
import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        height: "64px",
        backgroundColor: "white",
      }}
    >
      <Toolbar>
        <Typography
          variant="h5"
          component={Link}
          to="/"
          sx={{ flexGrow: 1, textDecoration: "none", color: "white" }}
        >
          ScholarSheets
        </Typography>
        <Button color="inherit" component={Link} to="/about">
          About
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
