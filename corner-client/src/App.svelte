<script lang="ts">
  import axios from "axios";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  import Guacamole from "guacamole-common-js";

  type Credentials = {
    username: string;
    password: string;
  };

  // Constants
  const API_URL = import.meta.env.VITE_API_URL;
  const TUNNEL_URL = import.meta.env.VITE_TUNNEL_URL;

  const GUAC_STATES = {
    IDLE: 0,
    CONNECTING: 1,
    WAITING: 2,
    CONNECTED: 3,
    DISCONNECTING: 4,
  };

  // Writable stores
  let loginMessage = writable("");

  // Variables
  let guacamoleClient: Guacamole.Client;
  const credentials = {
    username: "guacadmin",
    password: "guacadmin",
  };

  onMount(() => {
    loginAndInitializeRemoteDesktop();
  });

  async function loginAndInitializeRemoteDesktop() {
    try {
      const token = await login(credentials);
      initializeGuacamoleClient(token);
      loginMessage.set("Login successful");
    } catch (error) {
      if (error instanceof Error) {
        console.error("Login failed: ", error.message);
        loginMessage.set(`Login failed: ${error.message}`);
      } else {
        console.error("Login failed: ", error);
        loginMessage.set("Login failed: An unexpected error occurred");
      }
    }
  }

  async function login({ username, password }: Credentials) {
    const params = new URLSearchParams({ username, password });
    const config = {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    };
    const response = await axios.post(API_URL, params, config);
    return response.data.authToken; // Adjust based on actual response structure
  }

  function initializeGuacamoleClient(token: string) {
    guacamoleClient = new Guacamole.Client(
      new Guacamole.WebSocketTunnel(TUNNEL_URL)
    );
    setupKeyboardListeners();
    guacamoleClient.connect(
      `token=${token}&GUAC_ID=1&GUAC_TYPE=c&GUAC_DATA_SOURCE=mysql`
    );
    setupClientStateChangeListener();
  }

  function setupKeyboardListeners() {
    const keyboard = new Guacamole.Keyboard(document.body);
    keyboard.onkeydown = (keysym) => guacamoleClient.sendKeyEvent(1, keysym);
    keyboard.onkeyup = (keysym) => guacamoleClient.sendKeyEvent(0, keysym);
  }

  function setupClientStateChangeListener() {
    guacamoleClient.onstatechange = (state) => {
      const remoteDesktopContainer = document.getElementById(
        "remote-desktop-container"
      );
      // Check if remoteDesktopContainer is not null before proceeding
      if (remoteDesktopContainer) {
        switch (state) {
          case GUAC_STATES.CONNECTED:
            const displayElement = guacamoleClient.getDisplay().getElement();
            displayElement.style.zIndex = "1";
            remoteDesktopContainer.appendChild(displayElement);
            guacamoleClient.getDisplay().showCursor(true);
            break;
          case GUAC_STATES.DISCONNECTING:
          case GUAC_STATES.IDLE:
            remoteDesktopContainer.innerHTML = ""; // Safely clear the container
            break;
        }
      } else {
        // Optionally, handle the case when the element is not found
        console.error("Failed to find the remote desktop container element.");
      }
    };
  }
</script>

<main class="min-h-screen flex items-center justify-center bg-gray-50 px-6">
  <div id="remote-desktop-container" class="z-1"></div>
</main>
