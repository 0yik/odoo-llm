from odoo import models, fields, api, _


class LLMModel(models.Model):
    _name = "llm.model"
    _description = "LLM Model"
    _order = "sequence, id"

    name = fields.Char(string="Name", required=True)
    technical_name = fields.Char(string="Technical Name", required=True)
    provider_type = fields.Selection(
        [
            ("groq", "Groq"),
            ("openai", "OpenAI"),
            ("openrouter", "OpenRouter"),
        ],
        string="Provider Type",
        required=True,
    )
    context_length = fields.Integer(string="Context Length", help="Maximum context length in tokens")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(string="Sequence", default=10)

    _sql_constraints = [
        (
            "unique_technical_name",
            "UNIQUE(technical_name)",
            "Technical name must be unique!",
        ),
    ]
