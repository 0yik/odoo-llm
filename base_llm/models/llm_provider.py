import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class LLMProvider(models.Model):
    _name = "llm.provider"
    _description = "LLM Provider"

    name = fields.Char(string="Name", required=True)
    provider_type = fields.Selection(
        [
            ("groq", "Groq"),
            ("openai", "OpenAI"),
            ("openrouter", "OpenRouter"),
        ],
        string="Provider Type",
        required=True,
    )
    api_key = fields.Char(string="API Key")
    api_endpoint = fields.Char(string="API Endpoint")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    is_default = fields.Boolean(string="Default Provider")
    sequence = fields.Integer(string="Sequence", default=10)
    model_id = fields.Many2one(
        "llm.model",
        string="Model",
        required=True,
        domain="[('provider_type', '=', provider_type)]",
    )

    @api.onchange("provider_type")
    def _onchange_provider_type(self):
        """Reset model when provider type changes."""
        self.model_id = False

    @api.model
    def create(self, vals):
        if vals.get("is_default"):
            self.search(
                [
                    ("is_default", "=", True),
                    ("company_id", "=", vals.get("company_id", self.env.company.id)),
                ]
            ).write({"is_default": False})
        return super().create(vals)

    def write(self, vals):
        if vals.get("is_default"):
            self.search(
                [
                    ("is_default", "=", True),
                    ("company_id", "=", self.company_id.id),
                    ("id", "!=", self.id),
                ]
            ).write({"is_default": False})
        return super().write(vals)

    def process_prompt(self, prompt, **kwargs):
        """Process prompt using selected LLM provider."""
        self.ensure_one()

        if not self.api_key:
            raise UserError(_("API Key is required for LLM processing"))

        method_name = f"_process_{self.provider_type}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(prompt, **kwargs)
        else:
            raise UserError(
                _("Provider type %s is not implemented") % self.provider_type
            )

    @api.model
    def get_default_provider(self, company_id=None):
        """Get default LLM provider for company."""
        if not company_id:
            company_id = self.env.company.id
        return self.search(
            [("company_id", "=", company_id), ("is_default", "=", True)], limit=1
        )
