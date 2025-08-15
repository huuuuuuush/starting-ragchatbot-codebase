import anthropic
from typing import List, Optional, Dict, Any

class AIGenerator:
    """Handles interactions with Anthropic's Claude API for generating responses"""
    
    # Static system prompt to avoid rebuilding on each call
    SYSTEM_PROMPT = """ 你是一个专门处理课程材料和教育内容的人工智能助手，拥有全面的课程信息搜索工具。

可用工具：
1. **search_course_content**: 在课程材料中搜索特定内容
2. **get_course_outline**: 获取完整课程大纲，包括标题、课程链接和所有课程

工具使用指南：
- **search_course_content**: 用于关于特定课程内容、概念或详细教育材料的问题
- **get_course_outline**: 当用户询问课程结构、课程列表或"课程X包含什么"时使用
- **每个查询最多使用一个工具**
- 将工具结果合成为准确、基于事实的回答
- 如果工具没有找到结果，请清楚说明

回答协议：
- **一般知识问题**：使用现有知识回答，无需使用工具
- **课程特定问题**：使用适当的工具，然后回答
- **课程大纲**：使用get_course_outline工具提供完整的课程结构
- **无元评论**：
  - 仅提供直接答案 - 不要包含推理过程、工具解释或问题类型分析
  - 不要提及"基于工具结果"

对于课程大纲查询，包括：
- 课程标题和链接
- 带有编号和标题的完整课程列表
- 清晰格式化以便阅读

所有回答必须：
1. **简洁、简明、重点突出** - 快速切入要点
2. **教育性** - 保持教学价值
3. **清晰** - 使用易懂的语言
4. **示例支持** - 在有助于理解时包含相关示例
5. **使用简体中文** - 所有回复必须使用简体中文

仅提供对所问问题的直接答案。"""
    
    def __init__(self, api_key: str, model: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        
        # Pre-build base API parameters
        self.base_params = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 800
        }
    
    def generate_response(self, query: str,
                         conversation_history: Optional[str] = None,
                         tools: Optional[List] = None,
                         tool_manager=None) -> str:
        """
        Generate AI response with optional tool usage and conversation context.
        
        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            tools: Available tools the AI can use
            tool_manager: Manager to execute tools
            
        Returns:
            Generated response as string
        """
        
        # Build system content efficiently - avoid string ops when possible
        system_content = (
            f"{self.SYSTEM_PROMPT}\n\nPrevious conversation:\n{conversation_history}"
            if conversation_history 
            else self.SYSTEM_PROMPT
        )
        
        # Prepare API call parameters efficiently
        api_params = {
            **self.base_params,
            "messages": [{"role": "user", "content": query}],
            "system": system_content
        }
        
        # Add tools if available
        if tools:
            api_params["tools"] = tools
            api_params["tool_choice"] = {"type": "auto"}
        
        # Get response from Claude
        response = self.client.messages.create(**api_params)
        
        # Handle tool execution if needed
        if hasattr(response, 'stop_reason') and response.stop_reason == "tool_use" and tool_manager:
            return self._handle_tool_execution(response, api_params, tool_manager)
        
        # Return direct response
        return response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
    
    def _handle_tool_execution(self, initial_response, base_params: Dict[str, Any], tool_manager):
        """
        Handle execution of tool calls and get follow-up response.
        
        Args:
            initial_response: The response containing tool use requests
            base_params: Base API parameters
            tool_manager: Manager to execute tools
            
        Returns:
            Final response text after tool execution
        """
        # Start with existing messages
        messages = base_params["messages"].copy()
        
        # Add AI's tool use response
        messages.append({"role": "assistant", "content": initial_response.content})
        
        # Execute all tool calls and collect results
        tool_results = []
        for content_block in initial_response.content:
            if content_block.type == "tool_use":
                tool_result = tool_manager.execute_tool(
                    content_block.name, 
                    **content_block.input
                )
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": tool_result
                })
        
        # Add tool results as single message
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        
        # Prepare final API call without tools
        final_params = {
            **self.base_params,
            "messages": messages,
            "system": base_params["system"]
        }
        
        # Get final response
        final_response = self.client.messages.create(**final_params)
        return final_response.content[0].text if hasattr(final_response.content[0], 'text') else str(final_response.content[0])