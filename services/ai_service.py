import requests
from typing import Optional, Dict, Generator
from datetime import datetime, timezone, timedelta

class AIService:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys

    def chat(self, model: str, messages: list, system_prompt: str = "") -> dict:
        """Send chat request to specified model. Returns dict with 'content' and optional 'thinking'."""
        # Add current date/time to system prompt (北京时间 CST = UTC+8)
        utc_now = datetime.now(timezone.utc)
        cst = timezone(timedelta(hours=8))
        current_time = utc_now.astimezone(cst).strftime("%Y年%m月%d日 %H:%M:%S")
        time_info = f"当前日期时间(北京时间)：{current_time}"
        if system_prompt:
            system_prompt = f"{time_info}\n\n{system_prompt}"
        else:
            system_prompt = time_info
        model_lower = model.lower()
        if model_lower == "openai":
            return self._chat_openai(messages, system_prompt)
        elif model_lower == "deepseek":
            return self._chat_deepseek(messages, system_prompt)
        elif model_lower == "minimax":
            return self._chat_minimax(messages, system_prompt)
        elif model_lower == "claude":
            return self._chat_claude(messages, system_prompt)
        elif model_lower == "doubao":
            return self._chat_doubao(messages, system_prompt)
        elif model_lower == "kimi":
            return self._chat_kimi(messages, system_prompt)
        elif model_lower == "glm":
            return self._chat_glm(messages, system_prompt)
        elif model_lower == "qwen":
            return self._chat_qwen(messages, system_prompt)
        elif model_lower == "yuanbao":
            return self._chat_yuanbao(messages, system_prompt)
        elif model_lower == "gemini":
            return self._chat_gemini(messages, system_prompt)
        else:
            return {"content": f"[Error: Unknown model '{model}']", "thinking": None}

    def chat_stream(self, model: str, messages: list, system_prompt: str = ""):
        """Stream chat request to specified model. Yields text chunks."""
        utc_now = datetime.now(timezone.utc)
        cst = timezone(timedelta(hours=8))
        current_time = utc_now.astimezone(cst).strftime("%Y年%m月%d日 %H:%M:%S")
        time_info = f"当前日期时间(北京时间)：{current_time}"
        if system_prompt:
            system_prompt = f"{time_info}\n\n{system_prompt}"
        else:
            system_prompt = time_info
        model_lower = model.lower()
        
        if model_lower == "openai":
            yield from self._chat_openai_stream(messages, system_prompt)
        elif model_lower == "deepseek":
            yield from self._chat_deepseek_stream(messages, system_prompt)
        elif model_lower == "minimax":
            yield from self._chat_minimax_stream(messages, system_prompt)
        elif model_lower == "claude":
            yield from self._chat_claude_stream(messages, system_prompt)
        elif model_lower == "doubao":
            yield from self._chat_doubao_stream(messages, system_prompt)
        elif model_lower == "kimi":
            yield from self._chat_kimi_stream(messages, system_prompt)
        elif model_lower == "glm":
            yield from self._chat_glm_stream(messages, system_prompt)
        elif model_lower == "qwen":
            yield from self._chat_qwen_stream(messages, system_prompt)
        elif model_lower == "yuanbao":
            yield from self._chat_yuanbao_stream(messages, system_prompt)
        elif model_lower == "gemini":
            yield from self._chat_gemini_stream(messages, system_prompt)
        else:
            yield f"[Error: Unknown model '{model}']"

    def _get_messages_with_system(self, messages: list, system_prompt: str) -> list:
        """Add system prompt to messages"""
        if system_prompt:
            return [{"role": "system", "content": system_prompt}] + messages
        return messages

    def _chat_openai(self, messages: list, system_prompt: str) -> dict:
        """OpenAI Chat API (GPT-3.5/4)"""
        api_key = self.api_keys.get("openai")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Error: OpenAI API key not configured]", "thinking": None}

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return {"content": content, "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: OpenAI API request failed - {str(e)}]", "thinking": None}

    def _chat_deepseek(self, messages: list, system_prompt: str) -> dict:
        """DeepSeek Chat API with thinking process"""
        api_key = self.api_keys.get("deepseek")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Error: DeepSeek API key not configured]", "thinking": None}

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-v4-pro",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "max_tokens": 4096
            }
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            thinking = result.get("choices", [{}])[0].get("message", {}).get("reasoning_content", None)
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"content": content, "thinking": thinking}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: DeepSeek API request failed - {str(e)}]", "thinking": None}

    def _chat_minimax(self, messages: list, system_prompt: str, stream_callback=None) -> dict:
        """MiniMax Chat API (Anthropic-compatible)"""
        api_key = self.api_keys.get("minimax")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Error: MiniMax API key not configured]", "thinking": None}

        try:
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }

            minimax_messages = []
            for m in messages:
                minimax_messages.append({
                    "role": "user" if m["role"] == "user" else "assistant",
                    "content": m["content"]
                })

            data = {
                "model": "MiniMax-M3",
                "max_tokens": 8192,
                "messages": minimax_messages
            }

            if system_prompt:
                data["system"] = system_prompt

            # 流式输出
            if stream_callback:
                data["stream"] = True
                response = requests.post(
                    "https://api.minimaxi.com/anthropic/v1/messages",
                    headers=headers,
                    json=data,
                    stream=True,
                    timeout=120
                )
                response.raise_for_status()
                
                full_content = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith("data:"):
                            data_str = line[5:].strip()
                            if data_str and data_str != "[DONE]":
                                try:
                                    import json
                                    chunk = json.loads(data_str)
                                    if chunk.get("type") == "content_block_delta":
                                        delta = chunk.get("delta", {})
                                        if delta.get("type") == "text_delta":
                                            text = delta.get("text", "")
                                            full_content += text
                                            stream_callback(text)
                                except:
                                    pass
                
                return {"content": full_content, "thinking": None}
            else:
                response = requests.post(
                    "https://api.minimaxi.com/anthropic/v1/messages",
                    headers=headers,
                    json=data,
                    timeout=120
                )
                response.raise_for_status()
                result = response.json()

                if not result:
                    return {"content": "[Error: MiniMax API returned empty response]", "thinking": None}

                content = result.get("content", [])
                if isinstance(content, list):
                    for block in content:
                        if block.get("type") == "text":
                            return {"content": block.get("text", ""), "thinking": None}

                if "content" in result and isinstance(result["content"], str):
                    return {"content": result["content"], "thinking": None}

                return {"content": "[Error: MiniMax API response format unexpected]", "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: MiniMax API request failed - {str(e)}]", "thinking": None}
        except Exception as e:
            return {"content": f"[Error: MiniMax - {str(e)}]", "thinking": None}

    def _chat_claude(self, messages: list, system_prompt: str) -> dict:
        """Anthropic Claude API"""
        api_key = self.api_keys.get("anthropic")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Anthropic API key not configured]", "thinking": None}

        try:
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }

            claude_messages = []
            for m in messages:
                claude_messages.append({
                    "role": "user" if m["role"] == "user" else "assistant",
                    "content": m["content"]
                })

            data = {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 1024,
                "messages": claude_messages
            }

            if system_prompt:
                data["system"] = system_prompt

            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            return {"content": response.json()["content"][0]["text"], "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: Claude API request failed - {str(e)}]", "thinking": None}

    def _chat_doubao(self, messages: list, system_prompt: str) -> dict:
        """Doubao (豆包) API - 字节跳动火山引擎"""
        api_key = self.api_keys.get("doubao")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Doubao API key not configured]", "thinking": None}

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "doubao-pro-32k",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7
            }
            response = requests.post(
                "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            return {"content": response.json()["choices"][0]["message"]["content"], "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: Doubao API request failed - {str(e)}]", "thinking": None}

    def _chat_kimi(self, messages: list, system_prompt: str) -> dict:
        """Kimi (Moonshot) API"""
        api_key = self.api_keys.get("kimi")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Kimi API key not configured]", "thinking": None}

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "kimi-k2.6",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 1
            }
            response = requests.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            return {"content": response.json()["choices"][0]["message"]["content"], "thinking": None}
        except requests.exceptions.RequestException as e:
            error_detail = ""
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_detail = f" | Response: {e.response.text}"
                except Exception:
                    error_detail = f" | Status: {e.response.status_code}"
            return {"content": f"[Error: Kimi API request failed - {str(e)}{error_detail}]", "thinking": None}

    def _chat_glm(self, messages: list, system_prompt: str) -> dict:
        """GLM (智谱AI) API"""
        api_key = self.api_keys.get("glm")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[GLM API key not configured]", "thinking": None}

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "glm-5.2",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "max_tokens": 8192
            }
            response = requests.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers=headers,
                json=data,
                timeout=120
            )
            response.raise_for_status()
            return {"content": response.json()["choices"][0]["message"]["content"], "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: GLM API request failed - {str(e)}]", "thinking": None}

    def _chat_qwen(self, messages: list, system_prompt: str) -> dict:
        """Qwen (千问/通义千问) API"""
        api_key = self.api_keys.get("qwen")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Qwen API key not configured]", "thinking": None}

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "qwen-plus",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7
            }
            response = requests.post(
                "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            return {"content": response.json()["choices"][0]["message"]["content"], "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: Qwen API request failed - {str(e)}]", "thinking": None}

    def _chat_yuanbao(self, messages: list, system_prompt: str) -> dict:
        """Yuanbao (元宝/腾讯混元) API"""
        api_key = self.api_keys.get("yuanbao")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Yuanbao API key not configured]", "thinking": None}

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "hunyuan",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7
            }
            response = requests.post(
                "https://api.hunyuan.cloud.tencent.com/hunyuan/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            return {"content": response.json()["choices"][0]["message"]["content"], "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: Yuanbao API request failed - {str(e)}]", "thinking": None}

    def _chat_gemini(self, messages: list, system_prompt: str) -> dict:
        """Google Gemini API"""
        api_key = self.api_keys.get("gemini")
        if not api_key or not isinstance(api_key, str) or not api_key.strip():
            return {"content": "[Gemini API key not configured]", "thinking": None}

        try:
            headers = {
                "Content-Type": "application/json"
            }

            # Gemini API format
            gemini_messages = []
            for m in messages:
                gemini_messages.append({
                    "role": "user" if m["role"] == "user" else "model",
                    "parts": [{"text": m["content"]}]
                })

            data = {
                "contents": gemini_messages,
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 4096
                }
            }

            # Add system instruction if present
            if system_prompt:
                data["systemInstruction"] = {
                    "parts": [{"text": system_prompt}]
                }

            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return {"content": content, "thinking": None}
        except requests.exceptions.RequestException as e:
            return {"content": f"[Error: Gemini API request failed - {str(e)}]", "thinking": None}

    # ==================== STREAMING METHODS ====================

    def _chat_openai_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("openai")
        if not api_key or not api_key.strip():
            yield "[Error: OpenAI API key not configured]"
            return
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "stream": True
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        import json
                        try:
                            data_json = json.loads(data_str)
                            content = data_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_deepseek_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("deepseek")
        if not api_key or not api_key.strip():
            yield "[Error: DeepSeek API key not configured]"
            return
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "deepseek-v4-pro",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "max_tokens": 4096,
                "stream": True
            }
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers=headers,
                json=data,
                timeout=120,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        import json
                        try:
                            data_json = json.loads(data_str)
                            content = data_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_minimax_stream(self, messages: list, system_prompt: str):
        """MiniMax streaming chat - supports real SSE streaming"""
        api_key = self.api_keys.get("minimax")
        if not api_key or not api_key.strip():
            yield "[Error: MiniMax API key not configured]"
            return
        try:
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            minimax_messages = []
            for m in messages:
                minimax_messages.append({
                    "role": "user" if m["role"] == "user" else "assistant",
                    "content": m["content"]
                })
            data = {
                "model": "MiniMax-M3",
                "max_tokens": 8192,
                "stream": True,
                "messages": minimax_messages
            }
            if system_prompt:
                data["system"] = system_prompt
            response = requests.post(
                "https://api.minimaxi.com/anthropic/v1/messages",
                headers=headers,
                json=data,
                stream=True,
                timeout=120
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith("data:"):
                        data_str = line_str[5:].strip()
                        if data_str and data_str != "[DONE]":
                            try:
                                import json
                                chunk = json.loads(data_str)
                                if chunk.get("type") == "content_block_delta":
                                    delta = chunk.get("delta", {})
                                    if delta.get("type") == "text_delta":
                                        yield delta.get("text", "")
                            except:
                                pass
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_claude_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("anthropic")
        if not api_key or not api_key.strip():
            yield "[Error: Anthropic API key not configured]"
            return
        try:
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            claude_messages = []
            for m in messages:
                claude_messages.append({
                    "role": "user" if m["role"] == "user" else "assistant",
                    "content": m["content"]
                })
            data = {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 1024,
                "messages": claude_messages,
                "stream": True
            }
            if system_prompt:
                data["system"] = system_prompt
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            full_content = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        import json
                        try:
                            data_json = json.loads(line[6:])
                            delta = data_json.get("delta", {})
                            text = delta.get("text", "")
                            if text:
                                yield text
                                full_content += text
                        except:
                            pass
            if not full_content:
                yield "[Error: Claude streaming response empty]"
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_doubao_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("doubao")
        if not api_key or not api_key.strip():
            yield "[Error: Doubao API key not configured]"
            return
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "doubao-pro-32k",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "stream": True
            }
            response = requests.post(
                "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                headers=headers,
                json=data,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        import json
                        try:
                            data_json = json.loads(data_str)
                            content = data_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_kimi_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("kimi")
        if not api_key or not api_key.strip():
            yield "[Error: Kimi API key not configured]"
            return
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "kimi-k2.6",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 1,
                "stream": True
            }
            response = requests.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        import json
                        try:
                            data_json = json.loads(data_str)
                            content = data_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass
        except Exception as e:
            error_detail = ""
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_detail = f" | Response: {e.response.text}"
                except Exception:
                    error_detail = f" | Status: {e.response.status_code}"
            yield f"[Error: {str(e)}{error_detail}]"

    def _chat_glm_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("glm")
        if not api_key or not api_key.strip():
            yield "[Error: GLM API key not configured]"
            return
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "glm-5.2",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "max_tokens": 8192,
                "stream": True
            }
            response = requests.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers=headers,
                json=data,
                timeout=120,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        import json
                        try:
                            data_json = json.loads(data_str)
                            content = data_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_qwen_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("qwen")
        if not api_key or not api_key.strip():
            yield "[Error: Qwen API key not configured]"
            return
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "qwen-plus",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "stream": True
            }
            response = requests.post(
                "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        import json
                        try:
                            data_json = json.loads(data_str)
                            content = data_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_yuanbao_stream(self, messages: list, system_prompt: str):
        api_key = self.api_keys.get("yuanbao")
        if not api_key or not api_key.strip():
            yield "[Error: Yuanbao API key not configured]"
            return
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "hunyuan",
                "messages": self._get_messages_with_system(messages, system_prompt),
                "temperature": 0.7,
                "stream": True
            }
            response = requests.post(
                "https://api.hunyuan.cloud.tencent.com/hunyuan/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        import json
                        try:
                            data_json = json.loads(data_str)
                            content = data_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if content:
                                yield content
                        except:
                            pass
        except Exception as e:
            yield f"[Error: {str(e)}]"

    def _chat_gemini_stream(self, messages: list, system_prompt: str):
        # Gemini doesn't support true streaming via generateContent, return full response
        api_key = self.api_keys.get("gemini")
        if not api_key or not api_key.strip():
            yield "[Error: Gemini API key not configured]"
            return
        try:
            headers = {"Content-Type": "application/json"}
            gemini_messages = []
            for m in messages:
                gemini_messages.append({
                    "role": "user" if m["role"] == "user" else "model",
                    "parts": [{"text": m["content"]}]
                })
            data = {
                "contents": gemini_messages,
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
            }
            if system_prompt:
                data["systemInstruction"] = {"parts": [{"text": system_prompt}]}
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            # Stream character by character for effect
            for char in content:
                yield char
        except Exception as e:
            yield f"[Error: {str(e)}]"
