"use client";

import { useEffect, useState } from "react";

import { WS_URL } from "../lib/constants";

export default function useWebSocket() {
  const [prices, setPrices] = useState({});
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    let socket;
    let reconnectTimer;
    let stopped = false;

    function connect() {
      socket = new WebSocket(WS_URL);
      socket.onopen = () => setConnected(true);
      socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "snapshot") setPrices(message.prices || {});
        if (message.type === "tick" && message.symbol && message.price) {
          setPrices((current) => ({ ...current, [message.symbol]: message.price }));
        }
      };
      socket.onclose = () => {
        setConnected(false);
        if (!stopped) reconnectTimer = setTimeout(connect, 3000);
      };
      socket.onerror = () => socket.close();
    }

    connect();
    return () => {
      stopped = true;
      clearTimeout(reconnectTimer);
      socket?.close();
    };
  }, []);

  return { prices, connected };
}