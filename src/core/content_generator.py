"""
Content Generation Module

This module provides functionality to generate digital products from text input,
including ebooks, guides, courses, and other digital content.
"""

import json
import sys
import os
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.helpers import generate_id, sanitize_input, Logger


class DigitalProduct:
    """Represents a digital product generated from text."""
    
    def __init__(self, title, content, product_type="guide", tags=None):
        self.id = generate_id(title + str(datetime.now()))
        self.title = sanitize_input(title)
        self.content = sanitize_input(content)
        self.product_type = product_type
        self.tags = tags or []
        self.created_at = datetime.now()
        self.status = "draft"
        self.download_count = 0
        
    def publish(self):
        """Mark the product as published and ready for distribution."""
        self.status = "published"
        
    def to_dict(self):
        """Convert product to dictionary for storage/API."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "product_type": self.product_type,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "download_count": self.download_count
        }


class ContentGenerator:
    """Generates digital products from text input."""
    
    def __init__(self):
        self.products = []
        self.logger = Logger("ContentGenerator")
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load predefined templates for different product types."""
        return {
            "wellness_guide": {
                "structure": [
                    "Introduction",
                    "Understanding Wellness", 
                    "Practical Tips",
                    "Daily Practices",
                    "Resources",
                    "Conclusion"
                ],
                "tips": [
                    "Start with small, manageable changes",
                    "Focus on consistency over perfection",
                    "Listen to your body and mind",
                    "Seek support when needed"
                ]
            },
            "self_care_ebook": {
                "structure": [
                    "What is Self-Care?",
                    "Physical Self-Care",
                    "Mental Self-Care", 
                    "Emotional Self-Care",
                    "Creating Your Routine",
                    "Maintaining Balance"
                ],
                "tips": [
                    "Self-care is not selfish",
                    "Find what works for you personally",
                    "Schedule self-care like any other important activity",
                    "Start with just 10 minutes a day"
                ]
            },
            "productivity_guide": {
                "structure": [
                    "Setting Clear Goals",
                    "Time Management Techniques",
                    "Eliminating Distractions",
                    "Building Good Habits",
                    "Tools and Resources"
                ],
                "tips": [
                    "Focus on progress, not perfection",
                    "Use the 2-minute rule for small tasks",
                    "Batch similar activities together",
                    "Take regular breaks to maintain focus"
                ]
            }
        }
    
    def generate_product(self, text_input, product_type="guide", template_name=None):
        """Generate a digital product from text input."""
        self.logger.info(f"Generating {product_type} from text input")
        
        # Extract title from first line or use default
        lines = text_input.strip().split('\n')
        title = lines[0] if lines else f"Generated {product_type.title()}"
        content = '\n'.join(lines[1:]) if len(lines) > 1 else text_input
        
        # Apply template if specified
        if template_name and template_name in self.templates:
            content = self._apply_template(content, template_name)
            
        # Determine tags based on content and type
        tags = self._generate_tags(content, product_type)
        
        product = DigitalProduct(title, content, product_type, tags)
        self.products.append(product)
        
        self.logger.info(f"Created product: {product.title}")
        return product
    
    def _apply_template(self, content, template_name):
        """Apply a predefined template to structure the content."""
        template = self.templates[template_name]
        
        formatted_content = f"# {template_name.replace('_', ' ').title()}\n\n"
        
        # Add structure sections
        for section in template["structure"]:
            formatted_content += f"## {section}\n\n"
            formatted_content += content + "\n\n"
        
        # Add tips section
        formatted_content += "## Key Tips\n\n"
        for tip in template["tips"]:
            formatted_content += f"- {tip}\n"
        
        return formatted_content
    
    def _generate_tags(self, content, product_type):
        """Generate relevant tags based on content and type."""
        tags = [product_type]
        
        # Common wellness/self-care keywords
        wellness_keywords = {
            "wellness": ["wellness", "health", "wellbeing"],
            "self-care": ["self-care", "self care", "relaxation", "mindfulness"],
            "productivity": ["productivity", "efficiency", "goals", "habits"],
            "mental-health": ["mental health", "anxiety", "stress", "meditation"],
            "fitness": ["exercise", "fitness", "workout", "physical"]
        }
        
        content_lower = content.lower()
        for tag, keywords in wellness_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def get_products_by_type(self, product_type):
        """Get all products of a specific type."""
        return [p for p in self.products if p.product_type == product_type]
    
    def get_published_products(self):
        """Get all published products."""
        return [p for p in self.products if p.status == "published"]
    
    def search_products(self, query):
        """Search products by title, content, or tags."""
        query_lower = query.lower()
        results = []
        
        for product in self.products:
            if (query_lower in product.title.lower() or 
                query_lower in product.content.lower() or
                any(query_lower in tag.lower() for tag in product.tags)):
                results.append(product)
        
        return results