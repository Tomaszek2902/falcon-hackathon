import React, { useState } from "react";
import { Typography, Box } from "@mui/material";
import { Outlet } from "react-router-dom";
import DrawerMenu from "../components/Home/DrawerMenu";

const initialQueries = [
  {
    id: 1,
    query: "Sample Paper 1",
    difficulty: "easy",
    subject: "maths",
    questionFormat: "MCQ",
    numberOfQuestions: 10,
  },
  {
    id: 2,
    query: "Sample Paper 2",
    difficulty: "hard",
    subject: "english",
    questionFormat: "MCQ",
    numberOfQuestions: 10,
  },
  // Add more queries here
];

const drawerWidth = 240;

const Home = () => {
  const [queries, setQueries] = useState(initialQueries);

  return (
    <Box sx={{ display: "flex" }}>
      <DrawerMenu items={queries} />
      <Box component="main" sx={{ flexGrow: 1, p: 3, ml: `${drawerWidth}px` }}>
        <Outlet context={{ queries, setQueries }} />
      </Box>
    </Box>
  );
};

export default Home;
