import React from "react";
import { Container, Typography, Paper, Box } from "@mui/material";

const About = () => {
  return (
    <Container maxWidth="md" sx={{ marginTop: 4 }}>
      <Paper elevation={3} sx={{ padding: 3 }}>
        <Typography variant="h4" gutterBottom align="center">
          About Us
        </Typography>
        <Typography variant="body1" paragraph>
          Welcome to ScholarSheets, where we leverage cutting-edge GPT
          technology to help students and teachers generate practice exam papers
          with ease.
        </Typography>
        <Typography variant="body1" paragraph>
          Our mission is to make exam preparation more efficient and effective
          by providing customizable practice papers tailored to your needs.
          Whether you're a student looking to sharpen your skills or a teacher
          seeking to create diverse assessment materials, ScholarSheets has got
          you covered.
        </Typography>
        <Typography variant="body1" paragraph>
          Our app uses advanced AI to generate high-quality questions, allowing
          you to focus on learning and teaching without the hassle of manual
          question creation.
        </Typography>
        <Typography variant="body1" paragraph>
          Thank you for choosing ScholarSheets. We are committed to helping you
          achieve your academic goals with the power of AI!
        </Typography>
      </Paper>
    </Container>
  );
};

export default About;
