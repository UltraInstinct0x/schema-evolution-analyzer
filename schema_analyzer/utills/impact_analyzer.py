"""Impact analysis utilities"""

from typing import Dict, List, Any
import structlog

logger = structlog.get_logger()

class ImpactAnalyzer:
    """Analyzes impact of schema changes"""
    
    async def analyze_impact(self, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze impact of schema changes
        
        Args:
            changes: List of schema changes
            
        Returns:
            Impact analysis results
        """
        impact = {
            'severity': 'low',
            'breaking_changes': [],
            'data_loss_risk': False,
            'performance_impact': [],
            'migration_complexity': 'low'
        }
        
        breaking_changes = 0
        data_loss_risks = 0
        complex_changes = 0
        
        for change in changes:
            # Analyze breaking changes
            if change['type'] in ['table_removed', 'column_removed', 'column_type_changed']:
                breaking_changes += 1
                impact['breaking_changes'].append({
                    'type': change['type'],
                    'location': f"{change.get('table', '')}.{change.get('column', '')}"
                })
            
            # Analyze data loss risks
            if change['type'] in ['table_removed', 'column_removed']:
                data_loss_risks += 1
            
            # Analyze complexity
            if change['type'] in ['column_type_changed', 'table_removed']:
                complex_changes += 1
        
        # Determine overall severity
        if breaking_changes > 0:
            impact['severity'] = 'high'
        elif complex_changes > 0:
            impact['severity'] = 'medium'
        
        # Set data loss risk flag
        impact['data_loss_risk'] = data_loss_risks > 0
        
        # Determine migration complexity
        if complex_changes > 3:
            impact['migration_complexity'] = 'high'
        elif complex_changes > 0:
            impact['migration_complexity'] = 'medium'
        
        logger.info("Completed impact analysis",
                   severity=impact['severity'],
                   breaking_changes=breaking_changes,
                   data_loss_risk=impact['data_loss_risk'])
        
        return impact