"""Schema validation utilities"""

from typing import Dict, Any
import jsonschema
import structlog

logger = structlog.get_logger()

class SchemaValidator:
    """Validates database schema structure"""
    
    SCHEMA_DEFINITION = {
        "type": "object",
        "required": ["tables"],
        "properties": {
            "tables": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "columns"],
                    "properties": {
                        "name": {"type": "string"},
                        "columns": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name", "type"],
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"type": "string"},
                                    "nullable": {"type": "boolean"},
                                    "default": {"type": ["string", "number", "null"]},
                                    "constraints": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    async def validate(self, schema: Dict[str, Any]) -> None:
        """
        Validate schema against defined schema definition
        
        Args:
            schema: Database schema to validate
            
        Raises:
            jsonschema.exceptions.ValidationError: If schema is invalid
        """
        try:
            jsonschema.validate(schema, self.SCHEMA_DEFINITION)
            logger.info("Schema validation successful")
        except jsonschema.exceptions.ValidationError as e:
            logger.error("Schema validation failed", error=str(e))
            raise