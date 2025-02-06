// websocketService.js
export default class WebSocketService {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.reconnectTimeout = 3000; // 重连间隔时间
    }

    // 建立 WebSocket 连接
    connect() {
        this.ws = new WebSocket(this.url);
        this.ws.onopen = this.onOpen.bind(this);
        this.ws.onclose = this.onClose.bind(this);
        this.ws.onerror = this.onError.bind(this);
        this.ws.onmessage = this.onMessage.bind(this);
    }

    // WebSocket 连接成功
    onOpen(event) {
        console.log('WebSocket Connected');
    }

    // WebSocket 关闭
    onClose(event) {
        console.log('WebSocket Closed');
        setTimeout(() => this.connect(), this.reconnectTimeout); // 重连
    }

    // WebSocket 错误
    onError(event) {
        console.error('WebSocket Error: ', event);
    }

    // 处理消息
    onMessage(event) {
        console.log('WebSocket Message: ', event.data);
    }

    // 发送消息
    sendMessage(message) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(message);
        } else {
            console.error('WebSocket is not open');
        }
    }
}
