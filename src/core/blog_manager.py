"""
Blog System Module

This module handles blog functionality for wellness, self-care, 
and personal development content.
"""

import sys
import os
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.helpers import generate_id, sanitize_input, Logger


class BlogPost:
    """Represents a blog post."""
    
    def __init__(self, title, content, author="Admin", category="general", tags=None):
        self.id = generate_id(title + str(datetime.now()))
        self.title = sanitize_input(title)
        self.content = sanitize_input(content)
        self.author = sanitize_input(author)
        self.category = category
        self.tags = tags or []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.published = False
        self.views = 0
        self.featured = False
        
    def publish(self):
        """Publish the blog post."""
        self.published = True
        self.updated_at = datetime.now()
        
    def update_content(self, title=None, content=None, tags=None):
        """Update blog post content."""
        if title:
            self.title = sanitize_input(title)
        if content:
            self.content = sanitize_input(content)
        if tags:
            self.tags = tags
        self.updated_at = datetime.now()
        
    def increment_views(self):
        """Increment view count."""
        self.views += 1
        
    def to_dict(self):
        """Convert post to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "category": self.category,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "published": self.published,
            "views": self.views,
            "featured": self.featured
        }


class BlogManager:
    """Manages blog posts and content."""
    
    def __init__(self):
        self.posts = []
        self.categories = [
            "wellness", "self-care", "mental-health", "productivity", 
            "fitness", "nutrition", "mindfulness", "relationships", "general"
        ]
        self.logger = Logger("BlogManager")
        self._create_sample_posts()
        
    def _create_sample_posts(self):
        """Create some sample wellness blog posts."""
        sample_posts = [
            {
                "title": "5 Simple Daily Habits for Better Mental Wellness",
                "content": """Mental wellness is a journey, not a destination. Here are five simple habits you can incorporate into your daily routine to support your mental health:

**1. Morning Mindfulness (5 minutes)**
Start your day with 5 minutes of deep breathing or meditation. This helps center your mind and sets a positive tone for the day.

**2. Gratitude Practice**
Write down three things you're grateful for each day. This simple practice can shift your focus to the positive aspects of your life.

**3. Physical Movement**
Even a 10-minute walk can boost your mood and energy levels. Movement releases endorphins and helps reduce stress.

**4. Digital Boundaries**
Set specific times to check emails and social media. Constant connectivity can increase anxiety and stress levels.

**5. Evening Reflection**
Before bed, take a few minutes to reflect on your day. What went well? What did you learn? This helps process emotions and prepare for restful sleep.

Remember, small consistent actions lead to big changes over time. Start with one habit and gradually add others as they become routine.""",
                "category": "mental-health",
                "tags": ["mental-health", "wellness", "daily-habits", "mindfulness"]
            },
            {
                "title": "The Art of Self-Care: Beyond Bubble Baths",
                "content": """Self-care has become a buzzword, often reduced to spa days and bubble baths. While these can be wonderful, true self-care goes much deeper.

**Physical Self-Care**
- Regular exercise that you enjoy
- Nutritious meals that fuel your body
- Adequate sleep (7-9 hours for most adults)
- Regular medical check-ups

**Emotional Self-Care**
- Setting healthy boundaries
- Expressing your feelings through journaling or talking to trusted friends
- Practicing self-compassion
- Seeking therapy when needed

**Mental Self-Care**
- Learning new skills or hobbies
- Reading books that inspire you
- Limiting exposure to negative news or social media
- Practicing mindfulness and meditation

**Social Self-Care**
- Nurturing relationships that support you
- Setting boundaries with toxic relationships
- Making time for meaningful connections
- Asking for help when you need it

**Spiritual Self-Care**
- Connecting with nature
- Practicing gratitude
- Engaging in activities that give your life meaning
- Meditation or prayer, if that aligns with your beliefs

Self-care isn't selfish—it's essential. When you take care of yourself, you're better able to show up for others and handle life's challenges with resilience.""",
                "category": "self-care",
                "tags": ["self-care", "wellness", "mental-health", "boundaries"]
            },
            {
                "title": "Building Resilience: Your Mental Strength Training Guide",
                "content": """Resilience is like a muscle—the more you exercise it, the stronger it becomes. Here's how to build your mental resilience:

**1. Develop a Growth Mindset**
View challenges as opportunities to learn and grow rather than threats. Ask yourself, "What can I learn from this situation?"

**2. Build Strong Relationships**
Social support is crucial for resilience. Invest time in relationships with family, friends, and community members who support and encourage you.

**3. Practice Problem-Solving**
When faced with a challenge, break it down into smaller, manageable steps. Focus on what you can control and take action on those elements.

**4. Take Care of Your Physical Health**
Regular exercise, healthy eating, and adequate sleep provide the foundation for mental resilience. Your physical and mental health are interconnected.

**5. Develop Emotional Awareness**
Learn to recognize and name your emotions. This helps you respond thoughtfully rather than react impulsively to stressful situations.

**6. Find Meaning and Purpose**
Connect with your values and what matters most to you. Having a sense of purpose can help you navigate difficult times with greater resilience.

**7. Practice Mindfulness**
Stay present and aware of your thoughts and feelings without judgment. Mindfulness helps you respond to stress more effectively.

Remember, building resilience is an ongoing process. Be patient with yourself as you develop these skills.""",
                "category": "mental-health",
                "tags": ["resilience", "mental-health", "growth-mindset", "wellness"]
            },
            {
                "title": "Creating a Productive Yet Balanced Lifestyle",
                "content": """In our hustle culture, we often think productivity means working harder and longer. True productivity is about working smarter while maintaining balance and well-being.

**Redefine Productivity**
Productivity isn't about being busy—it's about making meaningful progress toward your goals while maintaining your health and relationships.

**Time Management Strategies**
- Use the Pomodoro Technique: 25 minutes of focused work followed by a 5-minute break
- Time-block your calendar for important tasks
- Batch similar activities together
- Learn to say no to commitments that don't align with your priorities

**Energy Management**
- Identify your peak energy hours and schedule important tasks then
- Take regular breaks to prevent burnout
- Alternate between high and low-energy activities
- Get enough sleep to maintain consistent energy levels

**Setting Boundaries**
- Create clear boundaries between work and personal time
- Communicate your limits to colleagues and clients
- Use technology mindfully—don't let it control your time
- Schedule downtime just as you would any other important appointment

**The 80/20 Rule**
Focus on the 20% of activities that produce 80% of your results. This helps you prioritize what truly matters and avoid getting caught up in busy work.

**Self-Care as Productivity**
Taking care of yourself isn't time away from productivity—it's what enables sustainable productivity. Regular self-care prevents burnout and keeps you performing at your best.

Remember, a balanced life is a productive life. Success includes not just professional achievements but also health, relationships, and personal fulfillment.""",
                "category": "productivity",
                "tags": ["productivity", "work-life-balance", "time-management", "wellness"]
            }
        ]
        
        for post_data in sample_posts:
            post = BlogPost(
                title=post_data["title"],
                content=post_data["content"],
                category=post_data["category"],
                tags=post_data["tags"]
            )
            post.publish()
            post.featured = True  # Mark sample posts as featured
            self.posts.append(post)
            
        self.logger.info(f"Created {len(sample_posts)} sample blog posts")
    
    def create_post(self, title, content, author="Admin", category="general", tags=None):
        """Create a new blog post."""
        post = BlogPost(title, content, author, category, tags)
        self.posts.append(post)
        self.logger.info(f"Created blog post: {post.title}")
        return post
    
    def get_published_posts(self):
        """Get all published posts, sorted by creation date (newest first)."""
        published = [post for post in self.posts if post.published]
        return sorted(published, key=lambda x: x.created_at, reverse=True)
    
    def get_posts_by_category(self, category):
        """Get all published posts in a specific category."""
        return [post for post in self.get_published_posts() if post.category == category]
    
    def get_featured_posts(self):
        """Get all featured posts."""
        return [post for post in self.get_published_posts() if post.featured]
    
    def search_posts(self, query):
        """Search posts by title, content, or tags."""
        query_lower = query.lower()
        results = []
        
        for post in self.get_published_posts():
            if (query_lower in post.title.lower() or 
                query_lower in post.content.lower() or
                any(query_lower in tag.lower() for tag in post.tags)):
                results.append(post)
        
        return results
    
    def get_post_by_id(self, post_id):
        """Get a specific post by ID."""
        for post in self.posts:
            if post.id == post_id:
                return post
        return None
    
    def get_recent_posts(self, limit=5):
        """Get the most recent published posts."""
        return self.get_published_posts()[:limit]
    
    def get_popular_posts(self, limit=5):
        """Get the most viewed posts."""
        published = self.get_published_posts()
        return sorted(published, key=lambda x: x.views, reverse=True)[:limit]