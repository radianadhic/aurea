/**
 * WebSocket client for real-time updates.
 * Connects to backend via STOMP-over-WebSocket.
 */
import { Client } from '@stomp/stompjs';
import auth from './auth.js';

class WebSocketClient {
  constructor() {
    this.client = null;
    this.connected = false;
    this.subscriptions = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 1000;
  }

  /**
   * Connect to WebSocket server
   */
  connect(url = null) {
    if (this.client?.active) return;

    const wsUrl =
      url ||
      (import.meta.env.VITE_WS_URL ||
        `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.hostname}:8080/ws`);

    this.client = new Client({
      brokerURL: wsUrl,
      connectHeaders: {
        Authorization: `Bearer ${auth.getAccessToken()}`,
      },
      reconnectDelay: this.reconnectDelay,
      heartbeatIncoming: 10000,
      heartbeatOutgoing: 10000,

      onConnect: () => {
        this.connected = true;
        this.reconnectAttempts = 0;
        console.log('WebSocket connected');
        window.dispatchEvent(new CustomEvent('ws:connected'));

        // Re-subscribe to previous topics
        this.subscriptions.forEach((callback, topic) => {
          this.subscribe(topic, callback);
        });
      },

      onDisconnect: () => {
        this.connected = false;
        console.log('WebSocket disconnected');
        window.dispatchEvent(new CustomEvent('ws:disconnected'));
      },

      onStompError: (frame) => {
        console.error('STOMP error:', frame.headers['message'], frame.body);
        window.dispatchEvent(
          new CustomEvent('ws:error', { detail: { error: frame.body } })
        );
      },

      onWebSocketClose: () => {
        this.connected = false;
        this.reconnectAttempts++;
        if (this.reconnectAttempts > this.maxReconnectAttempts) {
          console.warn('Max reconnect attempts reached');
        }
      },
    });

    this.client.activate();
  }

  /**
   * Disconnect
   */
  disconnect() {
    if (this.client) {
      this.client.deactivate();
      this.connected = false;
    }
  }

  /**
   * Subscribe to a topic
   */
  subscribe(topic, callback) {
    this.subscriptions.set(topic, callback);
    if (this.connected && this.client) {
      const sub = this.client.subscribe(topic, (message) => {
        try {
          const data = JSON.parse(message.body);
          callback(data);
        } catch (e) {
          console.error('Failed to parse WS message:', e);
        }
      });
      return sub;
    }
    return null;
  }

  /**
   * Unsubscribe from a topic
   */
  unsubscribe(topic) {
    this.subscriptions.delete(topic);
    // Note: STOMP subscription handle is in the client
  }

  /**
   * Send a message
   */
  send(destination, body) {
    if (this.connected && this.client) {
      this.client.publish({
        destination,
        body: JSON.stringify(body),
      });
    }
  }
}

export const ws = new WebSocketClient();
export default ws;
