import React from "react";
import { Drawer, List, ListItem, ListItemText, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";

const drawerWidth = 240;

const DrawerMenu = ({ items }) => {
  const navigate = useNavigate();

  const handleListItemClick = (id) => {
    navigate(`/queries/${id}`);
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
        {items.map((item) => (
          <ListItem
            button
            key={item.id}
            onClick={() => handleListItemClick(item.id)}
          >
            <ListItemText primary={item.query} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default DrawerMenu;
