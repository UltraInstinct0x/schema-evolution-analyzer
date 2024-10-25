"""Query validation utilities"""

from typing import Dict, List, Any
import sqlparse
import structlog

logger = structlog.get_logger()

class QueryValidator:
    """Validates SQL queries against schema"""
    
    async def validate_queries(
        self,
        queries: List[str],
        schema: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Validate SQL queries against new schema
        
        Args:
            queries: List of SQL queries to validate
            schema: Database schema to validate against
            
        Returns:
            List of validation results for each query
        """
        results = []
        schema_tables = {t['name']: t for t in schema['tables']}
        
        for query in queries:
            result = {
                'query': query,
                'is_valid': True,
                'errors': []
            }
            
            try:
                # Parse the SQL query
                parsed = sqlparse.parse(query)[0]
                
                # Extract table and column references
                tables_referenced = self._extract_table_references(parsed)
                columns_referenced = self._extract_column_references(parsed)
                
                # Validate table references
                for table in tables_referenced:
                    if table not in schema_tables:
                        result['is_valid'] = False
                        result['errors'].append(f"Referenced table not found: {table}")
                
                # Validate column references
                for table, column in columns_referenced:
                    if table in schema_tables:
                        schema_columns = {c['name'] for c in schema_tables[table]['columns']}
                        if column not in schema_columns:
                            result['is_valid'] = False
                            result['errors'].append(
                                f"Referenced column not found: {table}.{column}")
                
            except Exception as e:
                result['is_valid'] = False
                result['errors'].append(f"Query parsing error: {str(e)}")
            
            results.append(result)
        
        logger.info("Completed query validation",
                   num_queries=len(queries),
                   num_invalid=sum(1 for r in results if not r['is_valid']))
        
        return results
    
    def _extract_table_references(self, parsed_query: sqlparse.sql.Statement) -> List[str]:
        """Extract table references from parsed query"""
        # Simple implementation - should be enhanced for complex queries
        tables = []
        for token in parsed_query.flatten():
            if token.ttype is None and isinstance(token, sqlparse.sql.Identifier):
                tables.append(token.get_name())
        return tables
    
    def _extract_column_references(
        self,
        parsed_query: sqlparse.sql.Statement
    ) -> List[tuple[str, str]]:
        """Extract column references from parsed query"""
        # Simple implementation - should be enhanced for complex queries
        columns = []
        for token in parsed_query.flatten():
            if token.ttype is None and isinstance(token, sqlparse.sql.Identifier):
                parts = token.get_name().split('.')
                if len(parts) == 2:
                    columns.append((parts[0], parts[1]))
        return columns