<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" crossorigin="anonymous">
  <div class="main-container">
    <div class="chat-layout">
      <!-- 左侧边栏 -->
      <div class="sidebar">
        <div class="new-chat" @click="startNewChat">
          <i class="el-icon-plus"></i>
          新对话
        </div>
        <div class="history-list">
          <!-- 这里可以添加历史对话列表 -->
        </div>
      </div>

      <!-- 主聊天区域 -->
      <div class="chat-main">
        <div class="chat-header">
          <h2>DeepSeek Chat</h2>
        </div>
        
        <div class="messages-container" ref="messagesContainer">
          <template v-if="messages.length === 0">
            <div class="welcome-screen">
              <h1>DeepSeek AI Assistant</h1>
              <p>我是您的 AI 助手，让我们开始对话吧！</p>
            </div>
          </template>
          
          <div v-else v-for="(message, index) in messages" 
               :key="index" 
               class="message-wrapper"
               :class="message.sender">
            <div class="avatar">
              {{ message.sender === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <div class="message-text" v-if="message.sender === 'user'">
                {{ message.text }}
              </div>
              <div 
                class="message-text markdown-body" 
                v-else 
                :class="{ 'typing': message.isTyping }"
                v-html="message.displayText">
              </div>
              <div 
                v-if="message.reasoning_content" 
                class="reasoning-content markdown-body"
                :class="{ 'typing': message.isTyping }"
                v-html="message.displayReasoningContent">
              </div>
            </div>
          </div>
          
          <div v-if="isLoading" class="message-wrapper model">
            <div class="avatar">🤖</div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <div class="input-area">
          <div class="input-container">
            <el-input
              v-model="userInput"
              type="textarea"
              :rows="3"
              placeholder="输入您的问题..."
              @keyup.enter.ctrl="sendMessage"
              resize="none"
            />
            <div class="input-actions">
              <span class="hint">Ctrl + Enter 发送</span>
              <el-button 
                type="primary" 
                :disabled="!userInput.trim() || isLoading"
                @click="sendMessage">
                发送
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import OpenAI from "openai";
import MarkdownIt from 'markdown-it';
import mathjax3 from 'markdown-it-mathjax3';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css'; // 使用 GitHub 风格的代码高亮主题

const openai = new OpenAI({
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  apiKey: "sk-0ad365aa196641c7bd13fa65fdbf8663",
  dangerouslyAllowBrowser: true
});

// 使用 $$ 作为分隔符的数学公式示例
const formula = `
$$
r = \\frac{\\sum_{i=1}^{n}(x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum_{i=1}^{n}(x_i - \\bar{x})^2} \\sqrt{\\sum_{i=1}^{n}(y_i - \\bar{y})^2}}
$$
`;

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch (__) {}
    }
    return '';
  }
}).use(mathjax3);

export default {
  name: "DeepSeek",
  data() {
    return {
      messages: [],
      userInput: '',
      isLoading: false,
      typingSpeed: 30,
      isTyping: false,
    };
  },
  methods: {
    startNewChat() {
      this.messages = [];
      this.userInput = '';
    },
    async typeWriter(message, fullText, property) {
      this.isTyping = true;
      let currentText = '';
      const chars = fullText.split('');
      
      for (let char of chars) {
        currentText += char;
        // 使用 markdown 渲染器处理文本
        message[property] = this.renderMarkdown(currentText);
        await new Promise(resolve => setTimeout(resolve, this.typingSpeed));
        
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
      
      this.isTyping = false;
    },
    async sendMessage() {
      if (this.userInput.trim() === '' || this.isLoading) return;
      
      const userMessage = this.userInput.trim();
      this.messages.push({ 
        sender: 'user', 
        text: userMessage,
        displayText: userMessage 
      });
      
      this.userInput = '';
      this.isLoading = true;

      try {
        const response = await this.fetchResponse(userMessage);
        const modelMessage = {
          sender: 'model',
          text: response.content,
          displayText: '',
          reasoning_content: response.reasoning_content,
          displayReasoningContent: '',
          isTyping: true
        };
        
        this.messages.push(modelMessage);
        
        // 直接使用原始内容，让 typeWriter 处理渲染
        await this.typeWriter(modelMessage, response.content, 'displayText');
        
        if (response.reasoning_content) {
          await this.typeWriter(
            modelMessage, 
            response.reasoning_content, 
            'displayReasoningContent'
          );
        }
        
        modelMessage.isTyping = false;
      } catch (error) {
        console.error('Error:', error);
        this.messages.push({
          sender: 'model',
          text: '抱歉，发生了一些错误，请稍后重试。',
          displayText: '抱歉，发生了一些错误，请稍后重试。',
          isTyping: false
        });
      } finally {
        this.isLoading = false;
      }
    },
    async fetchResponse(input) {
      const completion = await openai.chat.completions.create({
        messages: [
          { 
            role: "system", 
            content: "You are a helpful assistant. When writing mathematical formulas, please use $$...$$" 
          },
          { role: "user", content: input }
        ],
        model: "deepseek-v3",
      });

      return {
        content: completion.choices[0].message.content,
        reasoning_content: completion.choices[0].message.reasoning_content
      };
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      container.scrollTop = container.scrollHeight;
    },
    renderMarkdown(text) {
      if (!text) return '';
      
      // 处理数学公式
      text = text
        // 处理块级公式，将 [...] 转换为 $$...$$
        .replace(/\[(.*?)\]/g, (match, p1) => `$$${p1}$$`)
        // 处理行内公式，将 (x_1) 这样的格式转换为 \(x_1\)
        .replace(/\$1\$/g, (match, p1) => `\\(${p1}\\)`);
      
      return md.render(text);
    },
    stripMarkdown(text) {
      return text.replace(/[#*`_\[\]]/g, '');
    }
  }
};
</script>

<style scoped>
.main-container {
  height: 100vh;
  background-color: #f7f7f8;
}

.chat-layout {
  display: flex;
  height: 100%;
}

.sidebar {
  width: 260px;
  background-color: #202123;
  padding: 20px;
  color: white;
}

.new-chat {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background-color: #343541;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.new-chat:hover {
  background-color: #40414f;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid #e5e5e5;
  background-color: #ffffff;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

.welcome-screen {
  text-align: center;
  padding: 40px;
  color: #444654;
}

.message-wrapper {
  display: flex;
  padding: 20px;
  gap: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.message-wrapper.user {
  background-color: #f7f7f8;
}

.message-wrapper.model {
  background-color: #ffffff;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background-color: #e5e5e5;
}

.message-content {
  flex: 1;
  line-height: 1.6;
}

.message-text {
  white-space: pre-wrap;
  color: #000000;  /* 设置为黑色 */
}

.message-wrapper.user .message-text {
  color: #000000;
}

.message-wrapper.model .message-text {
  color: #000000;
}

.reasoning-content {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 6px;
  font-size: 0.9em;
  color: #666;
}

.reasoning-header {
  font-weight: bold;
  margin-bottom: 5px;
  color: #444;
}

.input-area {
  padding: 20px;
  background-color: #ffffff;
  border-top: 1px solid #e5e5e5;
}

.input-container {
  max-width: 768px;
  margin: 0 auto;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.hint {
  color: #999;
  font-size: 0.9em;
}

.typing-indicator {
  display: flex;
  gap: 5px;
  padding: 10px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: #666;
  border-radius: 50%;
  animation: typing 1s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(2) { animation-delay: 0.3s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 添加 Markdown 样式 */
.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

.markdown-body pre {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
}

.markdown-body code {
  background-color: rgba(175, 184, 193, 0.2);
  border-radius: 6px;
  padding: 0.2em 0.4em;
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
}

.markdown-body p {
  margin-bottom: 16px;
  line-height: 1.6;
}

.markdown-body ul, .markdown-body ol {
  padding-left: 2em;
  margin-bottom: 16px;
}

.markdown-body table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 16px;
}

.markdown-body table th,
.markdown-body table td {
  padding: 6px 13px;
  border: 1px solid #d0d7de;
}

.markdown-body table tr {
  background-color: #ffffff;
  border-top: 1px solid #d0d7de;
}

.markdown-body table tr:nth-child(2n) {
  background-color: #f6f8fa;
}

.markdown-body blockquote {
  padding: 0 1em;
  color: #57606a;
  border-left: 0.25em solid #d0d7de;
  margin: 0 0 16px 0;
}

/* 修改打字机光标样式 */
.message-text.typing::after {
  content: '▋';
  display: inline-block;
  color: #000;
  animation: cursor .8s infinite;
  margin-left: 2px;
  vertical-align: middle;
}

@keyframes cursor {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 添加 MathJax 相关样式 */
.mjx-chtml {
  margin: 1em 0 !important;
  font-size: 1.1em !important;
}

.mjx-math {
  overflow-x: auto !important;
  overflow-y: hidden !important;
  max-width: 100% !important;
}
</style>
