"""Schema difference generation utilities"""

from typing import Dict, List, Any
import structlog

logger = structlog.get_logger()

class DiffGenerator:
    """Generates differences between database schemas"""
    
    async def generate_diff(
        self,
        old_schema: Dict[str, Any],
        new_schema: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate list of differences between old and new schemas
        
        Args:
            old_schema: Original database schema
            new_schema: Modified database schema
            
        Returns:
            List of schema changes
        """
        changes = []
        
        # Compare tables
        old_tables = {t['name']: t for t in old_schema['tables']}
        new_tables = {t['name']: t for t in new_schema['tables']}
        
        # Find removed tables
        for table_name in set(old_tables.keys()) - set(new_tables.keys()):
            changes.append({
                'type': 'table_removed',
                'table': table_name
            })
        
        # Find added tables
        for table_name in set(new_tables.keys()) - set(old_tables.keys()):
            changes.append({
                'type': 'table_added',
                'table': table_name
            })
        
        # Compare columns in existing tables
        for table_name in set(old_tables.keys()) & set(new_tables.keys()):
            old_columns = {c['name']: c for c in old_tables[table_name]['columns']}
            new_columns = {c['name']: c for c in new_tables[table_name]['columns']}
            
            # Find removed columns
            for col_name in set(old_columns.keys()) - set(new_columns.keys()):
                changes.append({
                    'type': 'column_removed',
                    'table': table_name,
                    'column': col_name
                })
            
            # Find added columns
            for col_name in set(new_columns.keys()) - set(old_columns.keys()):
                changes.append({
                    'type': 'column_added',
                    'table': table_name,
                    'column': col_name,
                    'column_details': new_columns[col_name]
                })
            
            # Compare modified columns
            for col_name in set(old_columns.keys()) & set(new_columns.keys()):
                old_col = old_columns[col_name]
                new_col = new_columns[col_name]
                
                if old_col['type'] != new_col['type']:
                    changes.append({
                        'type': 'column_type_changed',
                        'table': table_name,
                        'column': col_name,
                        'old_type': old_col['type'],
                        'new_type': new_col['type']
                    })
                
                if old_col.get('nullable') != new_col.get('nullable'):
                    changes.append({
                        'type': 'nullable_changed',
                        'table': table_name,
                        'column': col_name,
                        'old_nullable': old_col.get('nullable'),
                        'new_nullable': new_col.get('nullable')
                    })
        
        logger.info("Generated schema differences", num_changes=len(changes))
        return changes