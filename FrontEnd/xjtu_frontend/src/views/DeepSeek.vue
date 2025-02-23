<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" crossorigin="anonymous">
  <div class="main-container">
    <div class="chat-layout">
      <!-- 左侧边栏 -->
      <el-aside width="200px">
        <Sidebar />
      </el-aside>

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
            <template v-if="message.sender === 'model'">
              <div class="avatar">🤖</div>
              <div class="message-content">
                <div 
                  class="message-text markdown-body" 
                  v-html="message.displayText">
                </div>
                <div 
                  v-if="message.reasoning_content" 
                  class="reasoning-content markdown-body"
                  v-html="message.displayReasoningContent">
                </div>
              </div>
            </template>
            <template v-else>
              <div class="message-content user-message">
                <div class="message-text">
                  {{ message.text }}
                </div>
              </div>
              <div class="avatar user-avatar">👤</div>
            </template>
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
import katex from 'katex';
import 'katex/dist/katex.min.css';
import mk from 'markdown-it-katex';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import Sidebar from '../components/SideBar.vue';


const openai = new OpenAI({
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  apiKey: "sk-0ad365aa196641c7bd13fa65fdbf8663",
  dangerouslyAllowBrowser: true
});

// 修改 system prompt
const SYSTEM_PROMPT = `你是一个专业的助手。请直接用中文回答问题，不需要问候语，直接给出答案。遵循以下数学公式格式规则：

1. 对于块级公式（单独一行的公式），必须使用 $$....$$ 包裹，例如：

$$
\\text{Cov}(X, Y) = \\frac{1}{n} \\sum_{i=1}^n (x_i - \\bar{x})(y_i - \\bar{y})
$$

2. 对于行内公式，必须使用 $...$ 包裹，例如：
样本量为 $n$，均值为 $\\bar{x}$

3. 严格禁止使用 ()( 或其他格式包裹公式，只能使用：
- 块级公式：$$....$$
- 行内公式：$....$

请直接回答问题，给出清晰的解释和公式。`;

// 修改 markdown-it 配置
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
}).use(mk, {
  throwOnError: false,
  errorColor: '#cc0000',
  output: 'html'
});

export default {
  name: "DeepSeek",
  data() {
    return {
      messages: [],
      userInput: '',
      isLoading: false,
      currentMessageIndex: 0 // 添加: 用于跟踪当前显示的字符索引
    };
  },
  components: { Sidebar },
  methods: {

    async sendMessage() {
      if (this.userInput.trim() === '' || this.isLoading) return;
      
      const userMessage = this.userInput.trim();
      this.messages.push({ 
        sender: 'user', 
        text: userMessage
      });
      
      this.userInput = '';
      this.isLoading = true;

      try {
        const response = await this.fetchResponse(userMessage);
        const fullMessage = response.content;
        this.messages.push({
          sender: 'model',
          text: fullMessage,
          displayText: '',
          reasoning_content: response.reasoning_content,
          displayReasoningContent: response.reasoning_content ? 
            md.render(response.reasoning_content) : ''
        });
        this.currentMessageIndex = 0; // 重置索引
        this.typeWriter(fullMessage, this.messages.length - 1); // 调用 typeWriter 方法
      } catch (error) {
        console.error('Error:', error);
        this.messages.push({
          sender: 'model',
          text: '抱歉，发生了一些错误，请稍后重试。',
          displayText: '抱歉，发生了一些错误，请稍后重试。'
        });
      } finally {
        this.isLoading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    typeWriter(message, messageIndex) {
      if (this.currentMessageIndex < message.length) {
        this.messages[messageIndex].displayText += message.charAt(this.currentMessageIndex);
        this.currentMessageIndex++;
        setTimeout(() => this.typeWriter(message, messageIndex), 50); // 递归调用 typeWriter
      }
    },

    async fetchResponse(input) {
      const completion = await openai.chat.completions.create({
        messages: [
          { 
            role: "system", 
            content: SYSTEM_PROMPT 
          },
          {
            role: "user",
            content: input
          }
        ],  // 添加用户输入到消息列表中
        model: "deepseek-v3",
        temperature: 0.7,  // 添加温度参数来控制输出的创造性
        max_tokens: 2000   // 增加最大 token 数以确保完整输出
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
  display: flex;
  justify-content: flex-end;
  padding: 20px 40px;
  gap: 12px;
}

.message-wrapper.model {
  background-color: #ffffff;
  padding: 20px 20px 20px 40px;
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
  flex: 0 1 auto;
  line-height: 1.6;
  max-width: 80%;
  min-width: 0;
}

.message-text {
  white-space: pre-wrap;
  color: #000000;  /* 设置为黑色 */
}

.message-wrapper.user .message-text {
  background-color: #e3f2fd;
  padding: 10px 15px;
  border-radius: 15px;
  max-width: fit-content;
  margin: 0;
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

/* 添加 KaTeX 样式 */
.katex-display {
  overflow-x: auto;
  overflow-y: hidden;
  padding: 1em 0;
  margin: 0.5em 0;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.katex {
  font-size: 1.1em !important;
  text-rendering: auto;
  max-width: 100%;
}

.katex-html {
  overflow-x: auto;
  overflow-y: hidden;
  max-width: 100%;
}

/* 确保公式容器不会溢出 */
.message-content {
  overflow-x: auto;
  max-width: 100%;
}

/* 优化行内公式样式 */
.katex-inline {
  padding: 0.2em 0.1em;
  background-color: #f8f9fa;
  border-radius: 2px;
}
.main-container{
  height: 100vh;
  width: 100vw;
}

.user-message {
  margin: 0;
  display: flex;
  justify-content: flex-end;
}

.user-avatar {
  margin: 0;
  flex-shrink: 0;
}

.message-wrapper.user .message-content {
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.message-wrapper.user .message-text {
  background-color: #e3f2fd;
  padding: 10px 15px;
  border-radius: 15px;
  max-width: fit-content;
  margin: 0;
}
</style>
