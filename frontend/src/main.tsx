import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import { createRoot } from "react-dom/client";
import { App } from "./App";

const queryClient = new QueryClient();
const theme = createTheme({ palette: { primary: { main: "#155eef" } } });

createRoot(document.getElementById("root")!).render(
  <BrowserRouter><QueryClientProvider client={queryClient}><ThemeProvider theme={theme}><CssBaseline /><App /></ThemeProvider></QueryClientProvider></BrowserRouter>,
);
