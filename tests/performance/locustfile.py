"""Load testing configuration using Locust"""

from locust import HttpUser, task, between
from typing import Dict, Any
import json
import random

class SchemaAnalyzerUser(HttpUser):
    """Simulated user for load testing"""
    
    wait_time = between(1, 5)
    
    def on_start(self):
        """Setup before starting tests"""
        # Login and get authentication token
        response = self.client.post("/token", {
            "username": "test_user",
            "password": "test_password"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def analyze_schema(self):
        """Simulate schema analysis requests"""
        payload = self.generate_test_payload()
        self.client.post(
            "/analyze",
            json=payload,
            headers=self.headers
        )
    
    @task(1)
    def get_results(self):
        """Simulate result retrieval requests"""
        self.client.get(
            f"/results/{random.randint(1, 1000)}",
            headers=self.headers
        )
    
    def generate_test_payload(self) -> Dict[str, Any]:
        """Generate test payload for analysis"""
        return {
            "old_schema": {
                "tables": [
                    {
                        "name": f"table_{i}",
                        "columns": [
                            {
                                "name": f"column_{j}",
                                "type": random.choice(["INTEGER", "TEXT", "TIMESTAMP"])
                            }
                            for j in range(random.randint(3, 10))
                        ]
                    }
                    for i in range(random.randint(2, 5))
                ]
            },
            "new_schema": {
                "tables": [
                    {
                        "name": f"table_{i}",
                        "columns": [
                            {
                                "name": f"column_{j}",
                                "type": random.choice(["INTEGER", "TEXT", "TIMESTAMP"])
                            }
                            for j in range(random.randint(3, 10))
                        ]
                    }
                    for i in range(random.randint(2, 5))
                ]
            }
        }