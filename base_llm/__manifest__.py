{
    "name": "Base LLM",
    "version": "18.0.1.0.0",
    "category": "Technical",
    "summary": "Base module for LLM service integration",
    "description": """
        Base module for integrating Large Language Models (LLM) services.
        Supports multiple providers like Groq, OpenAI, OpenRouter, etc.
    """,
    "author": "Anang Aji Rahmawan",
    "website": "https://github.com/0yik",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/groq_llm_model_data.xml",
        "views/llm_provider_views.xml",
        "views/llm_model_views.xml",
    ],
    "external_dependencies": {
        "python": ["groq"],
    },
    "installable": True,
    "application": True,
}
