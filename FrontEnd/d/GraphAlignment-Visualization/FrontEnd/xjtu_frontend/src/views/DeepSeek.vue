<template>
  <!-- ... existing code ... -->
  <div class="message-content">
    <div class="message-text markdown-body" v-html="renderMarkdown(message.displayText)">
    </div>
    <div v-if="message.reasoning_content" class="reasoning-content markdown-body"
      v-html="renderMarkdown(message.displayReasoningContent)">
    </div>
  </div>
  <!-- ... existing code ... -->
</template>

<script>

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
  components: { Sidebar, Card },
  methods: {
    // 新增: Markdown 渲染方法
    renderMarkdown(content) {
      return md.render(content || '');
    },

    typeWriter(message, messageIndex) {
      if (this.currentMessageIndex < message.length) {
        const currentText = message.slice(0, this.currentMessageIndex + 1);
        this.messages[messageIndex].displayText = currentText;
        this.currentMessageIndex++;
        setTimeout(() => this.typeWriter(message, messageIndex), 50); // 递归调用 typeWriter
      } else {
        // 渲染完成后，确保 KaTeX 自动渲染
        this.$nextTick(() => {
          katex.renderMathInElement(this.$refs.messagesContainer, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false }
            ]
          });
        });
      }
    },

  }
};
</script>

<style scoped>
/* ... existing code ... */

/* 确保 Markdown 样式优先级 */
.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6;
  word-wrap: break-word;
}

/* 优化 KaTeX 公式样式 */
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

/* ... existing code ... */
</style>