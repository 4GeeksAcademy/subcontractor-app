// Import necessary components and functions from react-router-dom.

import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { Layout } from "./pages/Layout";
import { Home } from "./pages/Home";
import { Single } from "./pages/Single";
import { Demo } from "./pages/Demo";
import { Login } from "./pages/Login";
import { LoginProvider } from "./pages/LoginProvider";
import { SignUpClient } from "./pages/SignUpClient";
import { SignUpProvider } from "./pages/SignUpProvider";
import { ProviderDashboard } from "./pages/dashboardProvider/ProviderDashboard"
import { DashboardHome } from "./pages/dashboardProvider/DashboardHome"
import { PrivateProviderRoute } from "./pages/dashboardProvider/PrivateProviderRoute"
import { JobsPage } from "./pages/jobs"

export const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<Layout />} errorElement={<h1>Not found!</h1>} >

        {/* Nested Routes: Defines sub-routes within the BaseHome component. */}
        <Route path="/" element={<Home />} />
        <Route path="/single/:theId" element={<Single />} />  {/* Dynamic route for single items */}
        <Route path="/demo" element={<Demo />} />
        <Route path="/login" element={<Login />} />
        <Route path="/loginprovider" element={<LoginProvider />} />
        <Route path="/signupclient" element={<SignUpClient />} />

        <Route
          path="/providerdashboard"
          element={
            <PrivateProviderRoute>
              <ProviderDashboard />


            </PrivateProviderRoute>
          }
        >
          {/* Nested routes for dashboard sections */}
          <Route index element={<DashboardHome />} />
          <Route path="jobs" element={<JobsPage />} />
        </Route>

      </Route>

      <Route path="/signupprovider" element={<SignUpProvider />} />
    </>
  )
);