import axios from "axios";

export const setPaperService = async (subject, difficulty, formatQ, numQ) => {
  const url = `${import.meta.env.VITE_BACKEND_URL}/api/setPaper`;
  const data = {
    subject: subject,
    difficulty: difficulty,
    formatQ: formatQ,
    numQ: numQ,
  };

  try {
    const response = await axios.post(url, data);
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
};

export const generatePaperService = async (process_id) => {
  const url = `${import.meta.env.VITE_BACKEND_URL}/api/generate`;
  const data = {
    process_id: process_id,
  };

  try {
    const response = await axios.post(url, data, {
      responseType: "blob",
    });
    return response.data;
  } catch (error) {
    console.error(error);
  }
};
