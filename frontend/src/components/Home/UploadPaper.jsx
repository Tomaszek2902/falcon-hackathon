import React, { useState } from "react";
import { Button, Typography, Box } from "@mui/material";
import UploadPaperService from "../../services/UploadPaperService";

const UploadPaper = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  console.log(import.meta.env.VITE_BACKEND_URL);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setMessage("Please select a PDF file to upload.");
      return;
    }

    try {
      const response = await UploadPaperService.uploadExamPaper(file);
      setMessage("File uploaded successfully!");
      console.log(response);
    } catch (error) {
      console.log(error);
      setMessage("Error uploading file.");
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: "auto", mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Upload PDF
      </Typography>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          style={{ display: "none" }}
          id="upload-file"
        />
        <label htmlFor="upload-file">
          <Button variant="contained" component="span">
            Choose File
          </Button>
        </label>
        <Button type="submit" variant="contained" sx={{ ml: 2 }}>
          Upload
        </Button>
      </form>
      {message && <Typography mt={2}>{message}</Typography>}
    </Box>
  );
};

export default UploadPaper;
