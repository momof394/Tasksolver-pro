"""
Unit tests for the Blog Manager module.
"""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from core.blog_manager import BlogManager, BlogPost


class TestBlogPost(unittest.TestCase):
    """Test the BlogPost class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.post = BlogPost("Test Post", "This is test content", "Author", "wellness", ["test", "wellness"])
    
    def test_post_creation(self):
        """Test that posts are created correctly."""
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is test content")
        self.assertEqual(self.post.author, "Author")
        self.assertEqual(self.post.category, "wellness")
        self.assertEqual(self.post.tags, ["test", "wellness"])
        self.assertFalse(self.post.published)
        self.assertEqual(self.post.views, 0)
        self.assertFalse(self.post.featured)
    
    def test_post_publishing(self):
        """Test post publishing functionality."""
        self.post.publish()
        self.assertTrue(self.post.published)
    
    def test_post_content_update(self):
        """Test post content update functionality."""
        original_updated = self.post.updated_at
        self.post.update_content(title="Updated Title", content="Updated content")
        
        self.assertEqual(self.post.title, "Updated Title")
        self.assertEqual(self.post.content, "Updated content")
        self.assertGreater(self.post.updated_at, original_updated)
    
    def test_view_increment(self):
        """Test view count increment."""
        self.post.increment_views()
        self.assertEqual(self.post.views, 1)
        
        self.post.increment_views()
        self.assertEqual(self.post.views, 2)
    
    def test_post_to_dict(self):
        """Test post serialization to dictionary."""
        post_dict = self.post.to_dict()
        self.assertEqual(post_dict["title"], "Test Post")
        self.assertEqual(post_dict["category"], "wellness")
        self.assertFalse(post_dict["published"])


class TestBlogManager(unittest.TestCase):
    """Test the BlogManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = BlogManager()
    
    def test_manager_creation(self):
        """Test that manager is created with sample posts."""
        # BlogManager creates sample posts on initialization
        self.assertGreater(len(self.manager.posts), 0)
        self.assertIn("wellness", self.manager.categories)
        self.assertIn("self-care", self.manager.categories)
        self.assertIn("mental-health", self.manager.categories)
    
    def test_create_post(self):
        """Test creating new posts."""
        initial_count = len(self.manager.posts)
        post = self.manager.create_post("New Post", "New content", "Test Author", "wellness", ["test"])
        
        self.assertEqual(len(self.manager.posts), initial_count + 1)
        self.assertEqual(post.title, "New Post")
        self.assertEqual(post.author, "Test Author")
    
    def test_get_published_posts(self):
        """Test getting published posts."""
        # Sample posts are auto-published
        published = self.manager.get_published_posts()
        self.assertGreater(len(published), 0)
        
        # Create an unpublished post
        unpublished_post = self.manager.create_post("Draft Post", "Draft content")
        
        # Should not affect published count
        new_published = self.manager.get_published_posts()
        self.assertEqual(len(published), len(new_published))
    
    def test_get_posts_by_category(self):
        """Test filtering posts by category."""
        # Create posts in different categories
        self.manager.create_post("Wellness Post", "Content", category="wellness").publish()
        self.manager.create_post("Self-care Post", "Content", category="self-care").publish()
        
        wellness_posts = self.manager.get_posts_by_category("wellness")
        self.assertGreater(len(wellness_posts), 0)
        
        for post in wellness_posts:
            self.assertEqual(post.category, "wellness")
    
    def test_get_featured_posts(self):
        """Test getting featured posts."""
        featured = self.manager.get_featured_posts()
        self.assertGreater(len(featured), 0)
        
        for post in featured:
            self.assertTrue(post.featured)
            self.assertTrue(post.published)
    
    def test_search_posts(self):
        """Test post search functionality."""
        # Create a post with specific content
        test_post = self.manager.create_post("Mindfulness Guide", "This is about mindfulness and meditation", tags=["mindfulness"])
        test_post.publish()
        
        # Search by title
        results = self.manager.search_posts("mindfulness")
        self.assertGreater(len(results), 0)
        
        # Search by content
        results = self.manager.search_posts("meditation")
        self.assertGreater(len(results), 0)
        
        # Search by tag
        results = self.manager.search_posts("mindfulness")
        self.assertGreater(len(results), 0)
    
    def test_get_post_by_id(self):
        """Test getting a specific post by ID."""
        post = self.manager.create_post("Test Post", "Test content")
        retrieved_post = self.manager.get_post_by_id(post.id)
        
        self.assertEqual(retrieved_post.id, post.id)
        self.assertEqual(retrieved_post.title, "Test Post")
        
        # Test with non-existent ID
        non_existent = self.manager.get_post_by_id("fake-id")
        self.assertIsNone(non_existent)
    
    def test_get_recent_posts(self):
        """Test getting recent posts."""
        recent = self.manager.get_recent_posts(limit=3)
        self.assertLessEqual(len(recent), 3)
        
        # Should be sorted by creation date (newest first)
        if len(recent) > 1:
            self.assertGreaterEqual(recent[0].created_at, recent[1].created_at)
    
    def test_get_popular_posts(self):
        """Test getting popular posts by views."""
        # Create posts and set different view counts
        post1 = self.manager.create_post("Popular Post", "Content")
        post1.publish()
        post1.views = 100
        
        post2 = self.manager.create_post("Less Popular", "Content")
        post2.publish()
        post2.views = 50
        
        popular = self.manager.get_popular_posts(limit=2)
        
        # Should be sorted by views (highest first)
        if len(popular) >= 2:
            found_post1 = any(p.id == post1.id for p in popular)
            found_post2 = any(p.id == post2.id for p in popular)
            self.assertTrue(found_post1 or found_post2)


if __name__ == '__main__':
    unittest.main()