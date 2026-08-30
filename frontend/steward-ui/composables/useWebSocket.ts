/**
 * useWebSocket composable - Real-time WebSocket with auto-reconnect.
 */
import { ref, onUnmounted, computed } from 'vue';

export type WSStatus = 'connecting' | 'open' | 'closing' | 'closed' | 'error';

export interface WSMessage<T = any> {
  type: string;
  payload: T;
  timestamp: number;
  id?: string;
}

export interface WSOptions {
  url?: string;
  protocols?: string[];
  reconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeat?: boolean;
  heartbeatInterval?: number;
  heartbeatMessage?: string;
  onOpen?: (event: Event) => void;
  onClose?: (event: CloseEvent) => void;
  onError?: (event: Event) => void;
  onMessage?: (message: WSMessage) => void;
}

export function useWebSocket(options: WSOptions = {}) {
  const config = useRuntimeConfig();
  const defaultUrl = config.public.wsUrl || 'ws://localhost:8080/ws';

  const url = ref(options.url || defaultUrl);
  const status = ref<WSStatus>('closed');
  const lastMessage = ref<WSMessage | null>(null);
  const messages = ref<WSMessage[]>([]);
  const reconnectAttempts = ref(0);
  const lastError = ref<string | null>(null);

  let ws: WebSocket | null = null;
  let heartbeatTimer: any = null;
  let reconnectTimer: any = null;

  const isConnected = computed(() => status.value === 'open');

  function connect(overrideUrl?: string) {
    if (overrideUrl) url.value = overrideUrl;
    if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    try {
      status.value = 'connecting';
      ws = new WebSocket(url.value, options.protocols);

      ws.onopen = (event) => {
        status.value = 'open';
        reconnectAttempts.value = 0;
        lastError.value = null;
        if (options.heartbeat) startHeartbeat();
        options.onOpen?.(event);
      };

      ws.onclose = (event) => {
        status.value = 'closed';
        stopHeartbeat();
        options.onClose?.(event);
        if (options.reconnect && reconnectAttempts.value < (options.maxReconnectAttempts || 5)) {
          scheduleReconnect();
        }
      };

      ws.onerror = (event) => {
        status.value = 'error';
        lastError.value = 'WebSocket error';
        options.onError?.(event);
      };

      ws.onmessage = (event) => {
        try {
          const message: WSMessage = JSON.parse(event.data);
          lastMessage.value = message;
          messages.value.push(message);
          if (messages.value.length > 100) {
            messages.value = messages.value.slice(-100);
          }
          if (options.heartbeat && message.type === 'pong') return; // Skip heartbeat response
          options.onMessage?.(message);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };
    } catch (e: any) {
      status.value = 'error';
      lastError.value = e.message;
    }
  }

  function disconnect() {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    if (ws) {
      status.value = 'closing';
      ws.close();
      ws = null;
    }
  }

  function send(data: any) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      const message = typeof data === 'string' ? data : JSON.stringify(data);
      ws.send(message);
      return true;
    }
    return false;
  }

  function subscribe(topic: string, handler: (msg: WSMessage) => void) {
    send({ type: 'subscribe', topic });
    const wrapped = (msg: WSMessage) => {
      if (msg.type === topic || msg.payload?.topic === topic) {
        handler(msg);
      }
    };
    if (ws) ws.addEventListener('message', wrapped as any);
    return () => {
      if (ws) ws.removeEventListener('message', wrapped as any);
    };
  }

  function startHeartbeat() {
    heartbeatTimer = setInterval(() => {
      send({ type: 'ping', timestamp: Date.now() });
    }, options.heartbeatInterval || 30000);
  }

  function stopHeartbeat() {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer);
      heartbeatTimer = null;
    }
  }

  function scheduleReconnect() {
    reconnectAttempts.value++;
    const delay = (options.reconnectInterval || 3000) * reconnectAttempts.value;
    reconnectTimer = setTimeout(() => {
      connect();
    }, delay);
  }

  onUnmounted(() => {
    disconnect();
  });

  return {
    status: computed(() => status.value),
    isConnected,
    lastMessage,
    messages,
    reconnectAttempts,
    lastError,
    connect,
    disconnect,
    send,
    subscribe,
  };
}
