import axios from "axios";

const UploadPaperService = {
  uploadExamPaper: async (file, process_id) => {
    try {
      const formData = new FormData();
      formData.append("process_id", process_id);
      formData.append("content", file);

      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/uploadContent`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error("Error uploading exam paper:", error);
      throw error;
    }
  },
};

export default UploadPaperService;
