<script>
  import "./app.scss";

  // Routes - User
  import Home from "./routes/HomePage.svelte";
  import Register from "./routes/RegisterPage.svelte";
  import Token from "./routes/RequestPage.svelte";
  import NotFound from "./routes/NotFound.svelte";

  // Router
  import Router, { location } from "svelte-spa-router";
  import Footer from "./components/Footer.svelte";
  import NavigationBar from "./components/NavigationBar.svelte";
  let navBrand = "CVIS";
  let sideBarTitle = "Covid-19 Vaccination Information System";

  let navItems = [
    { url: "/", text: "Home" },
    { url: "/register", text: "Register" },
    { url: "/request-id", text: "Request ID" },
  ];

  let routes = {
    "/": Home,
    "/register": Register,
    "/request-id": Token,
    "*": NotFound,
  };
</script>

<NavigationBar {navBrand} {sideBarTitle} {navItems} currentURL={$location} />

<main class="container d-flex flex-column">
  <Router {routes} restoreScrollState={true} />
</main>

<Footer footerBrand={navBrand} />
