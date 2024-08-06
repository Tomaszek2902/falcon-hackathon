import React from "react";
import { Button, Drawer, List, ListItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { generatePaperService } from "../../services/SetAndGenerateService";
import { saveAs } from "file-saver";

const drawerWidth = 240;

const DrawerMenu = ({ tabs, processId }) => {
  const navigate = useNavigate();

  const handleListItemClick = (id) => {
    navigate(`/tabs/${id}`);
  };

  const handleGeneratePaperClick = async () => {
    try {
      const response = await generatePaperService(processId);
      const blob = new Blob([response], { type: "application/pdf" });
      saveAs(blob, "generated-paper.pdf");
    } catch (error) {
      console.error("Error generating paper:", error);
    }
  };

  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
          marginTop: `64px`,
        },
      }}
      variant="permanent"
      anchor="left"
    >
      <List>
        {tabs.map((tab) => (
          <ListItem
            key={tab.id}
            onClick={() => handleListItemClick(tab.id)}
            button
          >
            {tab.query}
          </ListItem>
        ))}
      </List>
      <Button
        sx={{ width: "80%", margin: `20px` }}
        onClick={handleGeneratePaperClick}
      >
        Generate Paper
      </Button>
    </Drawer>
  );
};

export default DrawerMenu;
