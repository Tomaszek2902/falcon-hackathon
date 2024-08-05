import React, { useState } from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { setPaperService } from "../services/SetAndGenerateService";
import { useOutletContext } from "react-router-dom";

export const QueryDetails = () => {
  const [subject, setSubject] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [formatQ, setFormatQ] = useState("");
  const [numQ, setNumQ] = useState("");

  const { setProcessId } = useOutletContext();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await setPaperService(subject, difficulty, formatQ, numQ);
    setProcessId(response.process_id);
  };

  return (
    <Container maxWidth="sm" sx={{ p: 4, backgroundColor: "white" }}>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" sx={{ color: "black" }} gutterBottom>
          Exam Paper Settings
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            margin="normal"
            variant="outlined"
            sx={{ backgroundColor: "white" }}
          />
          <TextField
            fullWidth
            label="Difficulty"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            margin="normal"
            variant="outlined"
            sx={{ backgroundColor: "white" }}
          />
          <TextField
            fullWidth
            label="Format of Questions"
            value={formatQ}
            onChange={(e) => setFormatQ(e.target.value)}
            margin="normal"
            variant="outlined"
            sx={{ backgroundColor: "white" }}
          />
          <TextField
            fullWidth
            label="Number of Questions"
            value={numQ}
            onChange={(e) => setNumQ(e.target.value)}
            margin="normal"
            variant="outlined"
            sx={{ backgroundColor: "white" }}
          />
          <Box sx={{ mt: 2 }}>
            <Button
              variant="contained"
              color="primary"
              type="submit"
              sx={{ backgroundColor: "white" }}
              fullWidth
            >
              Submit
            </Button>
          </Box>
        </form>
      </Box>
    </Container>
  );
};

export default QueryDetails;
