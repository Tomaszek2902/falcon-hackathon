import React, { useState } from "react";
import { Box } from "@mui/material";
import { Outlet } from "react-router-dom";
import DrawerMenu from "../components/Home/DrawerMenu";

const tabs = [
  {
    id: 1,
    query: "Set Paper Format",
  },
  {
    id: 2,
    query: "Upload Past Year Papers",
  },
  {
    id: 3,
    query: "Generate Question Paper",
  },
];

const drawerWidth = 240;

const Home = () => {
  const [processId, setProcessId] = useState();

  return (
    <Box sx={{ display: "flex" }}>
      <DrawerMenu tabs={tabs} setProcessId={setProcessId} />
      <Box component="main" sx={{ flexGrow: 1, p: 3, ml: `${drawerWidth}px` }}>
        <Outlet processId={processId} />
      </Box>
    </Box>
  );
};

export default Home;
