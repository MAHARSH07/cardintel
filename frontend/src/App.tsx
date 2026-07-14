import { AppBar, Box, Button, Container, Toolbar, Typography } from "@mui/material";
import { Link, Route, Routes } from "react-router-dom";

function Home() {
  return <Container sx={{ py: 8 }}><Typography variant="h2" gutterBottom>Find the right credit card.</Typography><Typography color="text.secondary">Compare cards, explore benefits, and get recommendations built around your spending.</Typography></Container>;
}

function Placeholder({ title }: { title: string }) {
  return <Container sx={{ py: 8 }}><Typography variant="h3">{title}</Typography><Typography color="text.secondary">This v1.0 module is ready for implementation.</Typography></Container>;
}

export function App() {
  return <Box><AppBar position="static"><Toolbar><Typography component={Link} to="/" variant="h6" sx={{ color: "inherit", textDecoration: "none", flexGrow: 1 }}>CardIntel</Typography><Button color="inherit" component={Link} to="/cards">Cards</Button><Button color="inherit" component={Link} to="/recommendations">Recommendations</Button></Toolbar></AppBar><Routes><Route path="/" element={<Home />} /><Route path="/cards" element={<Placeholder title="Card search" />} /><Route path="/recommendations" element={<Placeholder title="Recommendations" />} /><Route path="*" element={<Home />} /></Routes></Box>;
}
