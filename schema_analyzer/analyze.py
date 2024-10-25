"""Core schema analysis functionality"""

from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
from .metrics import instrument_method, ANALYSIS_DURATION
import structlog
from .utils.schema_validator import SchemaValidator
from .utils.diff_generator import DiffGenerator
from .utils.impact_analyzer import ImpactAnalyzer
from .utils.query_validator import QueryValidator

logger = structlog.get_logger()

class SchemaAnalyzer:
    """Main schema analysis orchestrator"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.schema_validator = SchemaValidator()
        self.diff_generator = DiffGenerator()
        self.impact_analyzer = ImpactAnalyzer()
        self.query_validator = QueryValidator()
    
    @instrument_method(ANALYSIS_DURATION)
    async def analyze_schema_changes(
        self,
        old_schema: Dict[str, Any],
        new_schema: Dict[str, Any],
        queries: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze schema changes and their impact
        
        Args:
            old_schema: Original database schema
            new_schema: Modified database schema
            queries: Optional list of SQL queries to validate
            
        Returns:
            Analysis results including changes, impacts, and recommendations
        """
        logger.info("Starting schema analysis", 
                   old_schema_tables=len(old_schema.get('tables', [])),
                   new_schema_tables=len(new_schema.get('tables', [])))
        
        # Validate input schemas
        await self.schema_validator.validate(old_schema)
        await self.schema_validator.validate(new_schema)
        
        # Generate schema differences
        changes = await self.diff_generator.generate_diff(old_schema, new_schema)
        
        # Analyze impact of changes
        impact = await self.impact_analyzer.analyze_impact(changes)
        
        # Validate queries against new schema if provided
        query_validation = None
        if queries:
            query_validation = await self.query_validator.validate_queries(
                queries, new_schema
            )
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(changes, impact)
        
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'changes': changes,
            'impact': impact,
            'recommendations': recommendations,
        }
        
        if query_validation:
            result['query_validation'] = query_validation
            
        logger.info("Schema analysis completed",
                   num_changes=len(changes),
                   impact_level=impact.get('severity'))
        
        return result
    
    async def _generate_recommendations(
        self,
        changes: List[Dict[str, Any]],
        impact: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommendations based on changes and their impact"""
        recommendations = []
        
        for change in changes:
            if change['type'] == 'column_removed':
                recommendations.append({
                    'type': 'data_migration',
                    'description': f"Create data migration plan for removed column: {change['column']}",
                    'priority': 'high'
                })
            
            elif change['type'] == 'column_type_changed':
                recommendations.append({
                    'type': 'data_conversion',
                    'description': (f"Plan data conversion from {change['old_type']} "
                                  f"to {change['new_type']} for column: {change['column']}"),
                    'priority': 'medium'
                })
            
            elif change['type'] == 'table_removed':
                recommendations.append({
                    'type': 'backup',
                    'description': f"Backup data from table before removal: {change['table']}",
                    'priority': 'high'
                })
        
        if impact.get('severity') == 'high':
            recommendations.append({
                'type': 'testing',
                'description': "Conduct thorough testing with production data sample",
                'priority': 'high'
            })
        
        return recommendations