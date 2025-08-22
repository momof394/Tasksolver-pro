"""
Web Application Module

Simple Flask web interface for the digital product generator and blog system.
"""

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.content_generator import ContentGenerator
from core.blog_manager import BlogManager
from utils.helpers import Logger


app = Flask(__name__)
app.secret_key = 'tasksolver-pro-wellness-app'

# Initialize our modules
content_generator = ContentGenerator()
blog_manager = BlogManager()
logger = Logger("WebApp")


@app.route('/')
def home():
    """Home page with featured content."""
    featured_posts = blog_manager.get_featured_posts()
    recent_products = content_generator.get_published_products()[:3]
    
    return render_template('home.html', 
                         featured_posts=featured_posts,
                         recent_products=recent_products)


@app.route('/generator')
def generator():
    """Content generator page."""
    return render_template('generator.html')


@app.route('/generate', methods=['POST'])
def generate_content():
    """Generate digital product from text input."""
    try:
        text_input = request.form.get('text_input', '').strip()
        product_type = request.form.get('product_type', 'guide')
        template_name = request.form.get('template_name', '')
        
        if not text_input:
            return jsonify({'error': 'Please provide text input'}), 400
        
        # Generate the product
        template = template_name if template_name != 'none' else None
        product = content_generator.generate_product(text_input, product_type, template)
        
        # Auto-publish for demo purposes
        product.publish()
        
        logger.info(f"Generated product: {product.title}")
        
        return jsonify({
            'success': True,
            'product': product.to_dict(),
            'message': f'Successfully generated {product_type}: {product.title}'
        })
        
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        return jsonify({'error': 'Failed to generate content'}), 500


@app.route('/products')
def products():
    """View all digital products."""
    all_products = content_generator.get_published_products()
    return render_template('products.html', products=all_products)


@app.route('/product/<product_id>')
def view_product(product_id):
    """View a specific product."""
    product = None
    for p in content_generator.products:
        if p.id == product_id:
            product = p
            product.download_count += 1
            break
    
    if not product:
        return "Product not found", 404
        
    return render_template('product_detail.html', product=product)


@app.route('/blog')
def blog():
    """Blog listing page."""
    category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    if search_query:
        posts = blog_manager.search_posts(search_query)
    elif category:
        posts = blog_manager.get_posts_by_category(category)
    else:
        posts = blog_manager.get_published_posts()
    
    categories = blog_manager.categories
    return render_template('blog.html', posts=posts, categories=categories, 
                         current_category=category, search_query=search_query)


@app.route('/blog/<post_id>')
def view_post(post_id):
    """View a specific blog post."""
    post = blog_manager.get_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    
    post.increment_views()
    related_posts = blog_manager.get_posts_by_category(post.category)[:3]
    
    return render_template('blog_post.html', post=post, related_posts=related_posts)


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@app.route('/api/stats')
def api_stats():
    """API endpoint for site statistics."""
    stats = {
        'total_products': len(content_generator.get_published_products()),
        'total_posts': len(blog_manager.get_published_posts()),
        'total_downloads': sum(p.download_count for p in content_generator.products),
        'total_views': sum(p.views for p in blog_manager.posts)
    }
    return jsonify(stats)


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    logger.info("Starting Tasksolver-pro Wellness App")
    app.run(debug=True, host='0.0.0.0', port=5000)