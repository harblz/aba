# A Python file to store long JSON Schema strings
# Should change to different method


QUIZ_RESULTS_STORAGE = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "quizzes": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "object",
                    "properties": {
                        "number": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "array",
                                    "prefixItems": {
                                        "type": "object",
                                        "properties": {
                                            "#correct": {"type": "integer"},
                                            "total": {"type": "integer"},
                                            "time-elapsed": {"type": "string"},
                                            "key": {
                                                "type": "array",
                                                "prefixItems": {
                                                    "type": "object",
                                                    "properties": {
                                                        "question_id": {
                                                            "type": "integer"
                                                        },
                                                        "correct_id": {
                                                            "type": "integer"
                                                        },
                                                        "chosen_id": {
                                                            "type": "integer"
                                                        },
                                                    },
                                                    "required": [
                                                        "question_id",
                                                        "correct_id",
                                                        "chosen_id",
                                                    ],
                                                },
                                                "items": False,
                                            },
                                        },
                                    },
                                    "required": [
                                        "#correct",
                                        "total",
                                        "time-elapsed",
                                        "key",
                                    ],
                                }
                            },
                        },
                        "required": ["date"],
                    },
                },
                "required": ["number"],
            },
        },
        "required": ["code"],
    },
    "required": ["quizzes"],
}
