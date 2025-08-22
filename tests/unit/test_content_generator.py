"""
Unit tests for the Content Generator module.
"""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from core.content_generator import ContentGenerator, DigitalProduct


class TestDigitalProduct(unittest.TestCase):
    """Test the DigitalProduct class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.product = DigitalProduct("Test Guide", "This is test content", "guide", ["test", "wellness"])
    
    def test_product_creation(self):
        """Test that products are created correctly."""
        self.assertEqual(self.product.title, "Test Guide")
        self.assertEqual(self.product.content, "This is test content")
        self.assertEqual(self.product.product_type, "guide")
        self.assertEqual(self.product.tags, ["test", "wellness"])
        self.assertEqual(self.product.status, "draft")
        self.assertEqual(self.product.download_count, 0)
    
    def test_product_publishing(self):
        """Test product publishing functionality."""
        self.product.publish()
        self.assertEqual(self.product.status, "published")
    
    def test_product_to_dict(self):
        """Test product serialization to dictionary."""
        product_dict = self.product.to_dict()
        self.assertEqual(product_dict["title"], "Test Guide")
        self.assertEqual(product_dict["product_type"], "guide")
        self.assertEqual(product_dict["status"], "draft")


class TestContentGenerator(unittest.TestCase):
    """Test the ContentGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = ContentGenerator()
    
    def test_generator_creation(self):
        """Test that generator is created correctly."""
        self.assertEqual(len(self.generator.products), 0)
        self.assertIn("wellness_guide", self.generator.templates)
        self.assertIn("self_care_ebook", self.generator.templates)
    
    def test_generate_basic_product(self):
        """Test generating a basic product without template."""
        text_input = "Wellness Tips\nTake care of yourself daily"
        product = self.generator.generate_product(text_input, "guide")
        
        self.assertEqual(product.title, "Wellness Tips")
        self.assertEqual(product.content, "Take care of yourself daily")
        self.assertEqual(product.product_type, "guide")
        self.assertEqual(len(self.generator.products), 1)
    
    def test_generate_product_with_template(self):
        """Test generating a product with template."""
        text_input = "Self-care is important"
        product = self.generator.generate_product(text_input, "ebook", "wellness_guide")
        
        self.assertIn("wellness guide", product.content.lower())
        self.assertIn("self-care is important", product.content.lower())
        self.assertEqual(product.product_type, "ebook")
    
    def test_tag_generation(self):
        """Test that appropriate tags are generated."""
        text_input = "Meditation and mindfulness for wellness"
        product = self.generator.generate_product(text_input)
        
        # Should include product type tag
        self.assertIn("guide", product.tags)
        # Should include wellness-related tags
        self.assertTrue(any(tag in ["wellness", "mental-health"] for tag in product.tags))
    
    def test_get_products_by_type(self):
        """Test filtering products by type."""
        self.generator.generate_product("Guide content", "guide")
        self.generator.generate_product("Ebook content", "ebook")
        
        guides = self.generator.get_products_by_type("guide")
        ebooks = self.generator.get_products_by_type("ebook")
        
        self.assertEqual(len(guides), 1)
        self.assertEqual(len(ebooks), 1)
        self.assertEqual(guides[0].product_type, "guide")
        self.assertEqual(ebooks[0].product_type, "ebook")
    
    def test_get_published_products(self):
        """Test filtering published products."""
        product1 = self.generator.generate_product("Published content", "guide")
        product2 = self.generator.generate_product("Draft content", "ebook")
        
        product1.publish()
        # product2 remains as draft
        
        published = self.generator.get_published_products()
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0].status, "published")
    
    def test_search_products(self):
        """Test product search functionality."""
        # Create products with specific content
        product1 = self.generator.generate_product("Wellness guide for beginners")
        product1.tags.extend(["wellness", "beginner"])
        
        product2 = self.generator.generate_product("Advanced meditation techniques")
        product2.tags.extend(["meditation", "advanced"])
        
        # Search by title
        results = self.generator.search_products("wellness")
        self.assertEqual(len(results), 1)
        self.assertIn("wellness", results[0].title.lower())
        
        # Search by content
        results = self.generator.search_products("meditation")
        self.assertEqual(len(results), 1)
        self.assertIn("meditation", results[0].title.lower())
        
        # Search by tag
        results = self.generator.search_products("beginner")
        self.assertEqual(len(results), 1)
        self.assertIn("beginner", results[0].tags)


if __name__ == '__main__':
    unittest.main()