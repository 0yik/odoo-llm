import json
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class GroqProvider(models.Model):
    _inherit = "llm.provider"

    def _process_groq(self, prompt, **kwargs):
        """Process prompt using Groq API.
        
        Args:
            prompt (str): The prompt to process
            **kwargs: Additional arguments
                - temperature (float): Controls randomness (default: 0.1)
                - max_tokens (int): Maximum tokens to generate (default: 2000)
                - top_p (float): Controls diversity via nucleus sampling (default: 1.0)
                - stream (bool): Whether to stream responses (default: False)
                - response_format (dict): Response format configuration (e.g., {"type": "json_object"})
        """
        self.ensure_one()

        if not self.api_key:
            raise UserError(_("Groq API key is required"))

        try:
            import groq
            client = groq.Groq(api_key=self.api_key)

            completion_kwargs = {
                "messages": [{"role": "user", "content": prompt}],
                "model": self.model_id.technical_name,
                "temperature": kwargs.get("temperature", 0.1),
                "max_tokens": kwargs.get("max_tokens", 2000),
                "top_p": kwargs.get("top_p", 1.0),
                "stream": kwargs.get("stream", False),
            }

            # Add response_format if provided
            if kwargs.get("response_format"):
                completion_kwargs["response_format"] = kwargs["response_format"]

            chat_completion = client.chat.completions.create(**completion_kwargs)

            if chat_completion.choices:
                content = chat_completion.choices[0].message.content.strip()
                
                # Parse JSON if response_format is json_object
                if kwargs.get("response_format", {}).get("type") == "json_object":
                    try:
                        content = json.loads(content)
                    except json.JSONDecodeError as e:
                        _logger.error("Error decoding JSON response: %s", str(e))
                        return {
                            "success": False,
                            "error": f"Invalid JSON response: {str(e)}",
                        }
                
                return {
                    "success": True,
                    "content": content,
                }
            
            return {
                "success": False,
                "error": "No response from Groq",
            }

        except Exception as e:
            _logger.error("Error processing with Groq: %s", str(e))
            return {
                "success": False,
                "error": str(e),
            }
