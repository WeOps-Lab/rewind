MENUS = [
    {
        "client_id": "munchkin",
        "name": "OpsPilot",
        "url": "/opspilot/studio",
        "description": "Create roles for the OpsPilot app to manage data permissions, menu permissions, and feature permissions.",  # noqa
        "menus": [
            {
                "name": "Studio",
                "children": [
                    {"id": "bot_list", "name": "Bot-list", "operation": ["View", "Add", "Edit", "Delete"]},
                    {"id": "bot_settings", "name": "Bot-Setting", "operation": ["View", "Edit", "Save&Publish"]},
                    {"id": "bot_channel", "name": "Bot-Channel", "operation": ["View", "Setting"]},
                    {"id": "bot_conversation_log", "name": "Bot-Conversation-Log", "operation": ["View", "Mark"]},
                    {"id": "bot_statistics", "name": "Bot-Statistics", "operation": ["View"]},
                ],
            },
            {
                "name": "Knowledge",
                "children": [
                    {"id": "knowledge_list", "name": " Knowledge-list", "operation": ["View", "Add", "Edit", "Delete"]},
                    {
                        "id": "knowledge_document",
                        "name": " Knowledge-Document",
                        "operation": ["View", "Add", "Set", "Train", "Delete"],
                    },
                    {"id": "knowledge_testing", "name": " Knowledge-Testing", "operation": ["View", "Edit"]},
                    {"id": "knowledge_setting", "name": " Knowledge-Setting", "operation": ["View", "Edit"]},
                    {"id": "knowledge_api", "name": " Knowledge-API", "operation": ["View"]},
                ],
            },
            {
                "name": "Skill",
                "children": [
                    {"id": "skill_list", "name": "Skill-list", "operation": ["View", "Add", "Edit", "Delete"]},
                    {"id": "skill_setting", "name": "Skill-Setting", "operation": ["View", "Edit"]},
                    {"id": "skill_rule", "name": "Skill-Rule", "operation": ["View", "Add", "Edit", "Delete"]},
                    {"id": "skill_api", "name": "Skill-Api", "operation": ["View"]},
                ],
            },
            {
                "name": "Provide",
                "children": [
                    {"id": "provide_list", "name": "Provide-list", "operation": ["View", "Setting"]},
                ],
            },
            {
                "name": "Setting",
                "children": [
                    {"id": "api_secret_key", "name": "API Secret Key", "operation": ["View", "Add", "Delete"]},
                    {"id": "mange_quota", "name": "Mange Quota", "operation": ["View", "Add", "Edit", "Delete"]},
                    {"id": "my_quota", "name": "My Quota", "operation": ["View"]},
                ],
            },
        ],
        "roles": [
            {"name": "admin", "role_name": "munchkin_admin", "menus": []},
            {
                "name": "normal",
                "role_name": "munchkin_normal",
                "menus": [
                    "api_secret_key-View",
                    "bot_channel-View",
                    "bot_conversation_log-View",
                    "bot_list-View",
                    "bot_settings-View",
                    "bot_statistics-View",
                    "knowledge_api-View",
                    "knowledge_document-View",
                    "knowledge_list-View",
                    "knowledge_setting-View",
                    "knowledge_testing-View",
                    "mange_quota-View",
                    "my_quota-View",
                    "provide_list-View",
                    "skill_api-View",
                    "skill_list-View",
                    "skill_rule-View",
                    "skill_setting-View",
                ],
            },
        ],
    },
]
