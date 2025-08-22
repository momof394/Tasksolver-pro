#!/usr/bin/env python3
"""
Test script for the digital product generator and blog functionality.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.content_generator import ContentGenerator
from core.blog_manager import BlogManager
from utils.helpers import Logger


def test_content_generator():
    """Test the content generator functionality."""
    print("=" * 50)
    print("TESTING CONTENT GENERATOR")
    print("=" * 50)
    
    generator = ContentGenerator()
    logger = Logger("TestGenerator")
    
    # Test basic product generation
    logger.info("Testing basic product generation...")
    product1 = generator.generate_product(
        "Self-Care for Busy People\nFinding time for self-care can be challenging, but it's essential for maintaining your well-being.",
        "guide"
    )
    product1.publish()
    
    # Test product with template
    logger.info("Testing product with wellness template...")
    product2 = generator.generate_product(
        "Mindfulness practices can reduce stress and improve focus. Start with just 5 minutes daily.",
        "ebook",
        "wellness_guide"
    )
    product2.publish()
    
    # Display results
    print(f"\nGenerated {len(generator.products)} products:")
    for i, product in enumerate(generator.products, 1):
        print(f"\n{i}. {product.title}")
        print(f"   Type: {product.product_type}")
        print(f"   Status: {product.status}")
        print(f"   Tags: {', '.join(product.tags)}")
        print(f"   Content preview: {product.content[:100]}...")
    
    return generator


def test_blog_manager():
    """Test the blog manager functionality."""
    print("\n" + "=" * 50)
    print("TESTING BLOG MANAGER")
    print("=" * 50)
    
    blog = BlogManager()
    logger = Logger("TestBlog")
    
    # Test creating a new post
    logger.info("Testing blog post creation...")
    new_post = blog.create_post(
        "Digital Wellness in 2024",
        "As we become more connected digitally, it's important to maintain balance and practice digital wellness. Here are some tips for maintaining healthy technology habits...",
        "Admin",
        "wellness",
        ["digital-wellness", "technology", "balance"]
    )
    new_post.publish()
    
    # Display sample posts
    featured_posts = blog.get_featured_posts()
    print(f"\nBlog has {len(blog.posts)} total posts")
    print(f"Featured posts: {len(featured_posts)}")
    print(f"Categories: {', '.join(blog.categories)}")
    
    print("\nFeatured posts:")
    for i, post in enumerate(featured_posts[:3], 1):
        print(f"\n{i}. {post.title}")
        print(f"   Category: {post.category}")
        print(f"   Tags: {', '.join(post.tags)}")
        print(f"   Views: {post.views}")
        print(f"   Content preview: {post.content[:100]}...")
    
    return blog


def test_search_functionality(generator, blog):
    """Test search functionality across both systems."""
    print("\n" + "=" * 50)
    print("TESTING SEARCH FUNCTIONALITY")
    print("=" * 50)
    
    # Test product search
    wellness_products = generator.search_products("wellness")
    print(f"\nFound {len(wellness_products)} products matching 'wellness':")
    for product in wellness_products:
        print(f"  - {product.title} ({product.product_type})")
    
    # Test blog search
    wellness_posts = blog.search_posts("wellness")
    print(f"\nFound {len(wellness_posts)} blog posts matching 'wellness':")
    for post in wellness_posts:
        print(f"  - {post.title} ({post.category})")
    
    # Test category filtering
    mental_health_posts = blog.get_posts_by_category("mental-health")
    print(f"\nFound {len(mental_health_posts)} posts in 'mental-health' category:")
    for post in mental_health_posts:
        print(f"  - {post.title}")


def main():
    """Main test function."""
    print("TASKSOLVER PRO - DIGITAL PRODUCT GENERATOR & WELLNESS BLOG")
    print("Testing new functionality...")
    
    try:
        # Test content generator
        generator = test_content_generator()
        
        # Test blog manager
        blog = test_blog_manager()
        
        # Test search functionality
        test_search_functionality(generator, blog)
        
        print("\n" + "=" * 50)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nThe platform includes:")
        print("✓ Content generator for digital products")
        print("✓ Blog system with wellness content")
        print("✓ Search functionality")
        print("✓ Multiple product templates")
        print("✓ Free access to all features")
        print("\nTo start the web interface:")
        print("cd src/web && python3 app.py")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())