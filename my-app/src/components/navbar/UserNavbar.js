import "./UserNavbar.css"
import { Navbar, Nav, Button } from 'react-bootstrap';
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined";

const UserNavbar = ({ userEmail, onLogout }) => {
  return (
    <Navbar bg="light" expand="lg">
      <Navbar.Brand href="/home"><HomeOutlinedIcon /></Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse className="justify-content-end">
        <Nav>
          <Nav.Item className="mr-3">
            <span className="navbar-text">{userEmail}</span>
          </Nav.Item>
          <Nav.Item>
            <Button variant="outline-danger" onClick={onLogout}>
              Logout
            </Button>
          </Nav.Item>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default UserNavbar;
