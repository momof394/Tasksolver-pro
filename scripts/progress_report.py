#!/usr/bin/env python3
"""
Progress Report Generator for Tasksolver-pro

This script analyzes the current state of the project and generates
a comprehensive progress report showing what has been implemented,
what's working, and what capabilities are available.
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from core.task_manager import TaskManager
from utils.helpers import Logger


class ProjectAnalyzer:
    """Analyzes the current state of the Tasksolver-pro project."""
    
    def __init__(self):
        self.logger = Logger("ProgressAnalyzer")
        self.project_root = Path(__file__).parent.parent
        self.report_data = {}
    
    def analyze_code_structure(self):
        """Analyze the codebase structure and files."""
        code_stats = {
            'python_files': 0,
            'markdown_files': 0,
            'shell_scripts': 0,
            'total_lines': 0,
            'components': {}
        }
        
        # Analyze source code
        src_dir = self.project_root / 'src'
        if src_dir.exists():
            for py_file in src_dir.rglob('*.py'):
                code_stats['python_files'] += 1
                with open(py_file, 'r') as f:
                    lines = len(f.readlines())
                    code_stats['total_lines'] += lines
                    component = py_file.relative_to(src_dir).parts[0] if len(py_file.relative_to(src_dir).parts) > 1 else 'root'
                    if component not in code_stats['components']:
                        code_stats['components'][component] = 0
                    code_stats['components'][component] += lines
        
        # Count documentation files
        for md_file in self.project_root.rglob('*.md'):
            code_stats['markdown_files'] += 1
        
        # Count shell scripts
        for sh_file in self.project_root.rglob('*.sh'):
            code_stats['shell_scripts'] += 1
        
        self.report_data['code_structure'] = code_stats
    
    def test_functionality(self):
        """Test the current functionality."""
        test_results = {
            'unit_tests': {'status': 'unknown', 'count': 0},
            'examples': {'status': 'unknown', 'count': 0},
            'core_functionality': []
        }
        
        # Run unit tests
        try:
            result = subprocess.run([
                'python3', 'tests/unit/test_task_manager.py'
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                test_results['unit_tests']['status'] = 'passing'
                # Count tests from output
                if 'Ran' in result.stderr:
                    test_count = result.stderr.split('Ran ')[1].split(' ')[0]
                    test_results['unit_tests']['count'] = int(test_count)
            else:
                test_results['unit_tests']['status'] = 'failing'
        except Exception as e:
            test_results['unit_tests']['status'] = f'error: {str(e)}'
        
        # Test core functionality
        try:
            task_manager = TaskManager()
            
            # Test task creation
            task = task_manager.create_task("Test Task", "Test description", "high")
            test_results['core_functionality'].append("✓ Task creation")
            
            # Test task assignment
            task.assign("test_user")
            test_results['core_functionality'].append("✓ Task assignment")
            
            # Test task completion
            task.complete()
            test_results['core_functionality'].append("✓ Task completion")
            
            # Test filtering
            pending_tasks = task_manager.get_tasks_by_status("pending")
            completed_tasks = task_manager.get_tasks_by_status("completed")
            test_results['core_functionality'].append("✓ Task filtering by status")
            
            user_tasks = task_manager.get_tasks_by_user("test_user")
            test_results['core_functionality'].append("✓ Task filtering by user")
            
        except Exception as e:
            test_results['core_functionality'].append(f"✗ Error testing functionality: {str(e)}")
        
        # Check examples
        examples_dir = self.project_root / 'examples'
        if examples_dir.exists():
            example_count = len(list(examples_dir.rglob('main.py')))
            test_results['examples']['count'] = example_count
            
            # Try to run basic example
            try:
                result = subprocess.run([
                    'python3', 'examples/basic-usage/main.py'
                ], cwd=self.project_root, capture_output=True, text=True)
                
                if result.returncode == 0:
                    test_results['examples']['status'] = 'working'
                else:
                    test_results['examples']['status'] = 'failing'
            except Exception:
                test_results['examples']['status'] = 'error'
        
        self.report_data['functionality'] = test_results
    
    def analyze_documentation(self):
        """Analyze the documentation coverage."""
        docs_analysis = {
            'documentation_files': 0,
            'documentation_topics': [],
            'coverage_areas': {}
        }
        
        docs_dir = self.project_root / 'docs'
        if docs_dir.exists():
            for doc_file in docs_dir.glob('*.md'):
                docs_analysis['documentation_files'] += 1
                topic = doc_file.stem.replace('-', ' ').title()
                docs_analysis['documentation_topics'].append(topic)
        
        # Check for key documentation areas
        key_areas = {
            'getting-started': 'User Onboarding',
            'api-reference': 'API Documentation',
            'architecture': 'Technical Architecture',
            'team-structure': 'Organization Structure',
            'project-structure': 'Project Layout',
            'best-practices': 'Development Standards'
        }
        
        for filename, description in key_areas.items():
            file_path = docs_dir / f'{filename}.md'
            docs_analysis['coverage_areas'][description] = '✓' if file_path.exists() else '✗'
        
        self.report_data['documentation'] = docs_analysis
    
    def analyze_project_maturity(self):
        """Assess the overall project maturity."""
        maturity = {
            'development_stage': 'Early Development',
            'completed_features': [],
            'in_progress_features': [],
            'planned_features': [],
            'readiness_metrics': {}
        }
        
        # Assess completed features
        if self.report_data.get('functionality', {}).get('unit_tests', {}).get('status') == 'passing':
            maturity['completed_features'].append('Core Task Management')
            maturity['completed_features'].append('Unit Testing Framework')
        
        if self.report_data.get('functionality', {}).get('examples', {}).get('status') == 'working':
            maturity['completed_features'].append('Basic Usage Examples')
        
        if self.report_data.get('documentation', {}).get('documentation_files', 0) > 3:
            maturity['completed_features'].append('Comprehensive Documentation')
        
        # Assess readiness metrics
        total_tests = self.report_data.get('functionality', {}).get('unit_tests', {}).get('count', 0)
        maturity['readiness_metrics']['Test Coverage'] = f"{total_tests} unit tests"
        
        code_lines = self.report_data.get('code_structure', {}).get('total_lines', 0)
        maturity['readiness_metrics']['Code Base Size'] = f"{code_lines} lines of Python code"
        
        docs_count = self.report_data.get('documentation', {}).get('documentation_files', 0)
        maturity['readiness_metrics']['Documentation'] = f"{docs_count} documentation files"
        
        # Determine stage based on features
        if len(maturity['completed_features']) >= 4:
            maturity['development_stage'] = 'Beta/Pre-Production'
        elif len(maturity['completed_features']) >= 2:
            maturity['development_stage'] = 'Alpha/Active Development'
        else:
            maturity['development_stage'] = 'Initial/Prototype'
        
        self.report_data['maturity'] = maturity
    
    def generate_report(self):
        """Generate and display the complete progress report."""
        print("=" * 70)
        print("TASKSOLVER-PRO PROJECT PROGRESS REPORT")
        print("=" * 70)
        print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Project Overview
        print("📊 PROJECT OVERVIEW")
        print("-" * 50)
        maturity = self.report_data.get('maturity', {})
        print(f"Development Stage: {maturity.get('development_stage', 'Unknown')}")
        print(f"Project Root: {self.project_root}")
        print()
        
        # Code Structure
        print("💻 CODEBASE ANALYSIS")
        print("-" * 50)
        code_stats = self.report_data.get('code_structure', {})
        print(f"Python Files: {code_stats.get('python_files', 0)}")
        print(f"Total Lines of Code: {code_stats.get('total_lines', 0)}")
        print(f"Documentation Files: {code_stats.get('markdown_files', 0)}")
        print(f"Shell Scripts: {code_stats.get('shell_scripts', 0)}")
        
        if code_stats.get('components'):
            print("\nCode Components:")
            for component, lines in code_stats['components'].items():
                print(f"  • {component}: {lines} lines")
        print()
        
        # Functionality Status
        print("⚙️  FUNCTIONALITY STATUS")
        print("-" * 50)
        functionality = self.report_data.get('functionality', {})
        
        unit_tests = functionality.get('unit_tests', {})
        print(f"Unit Tests: {unit_tests.get('status', 'unknown')} ({unit_tests.get('count', 0)} tests)")
        
        examples = functionality.get('examples', {})
        print(f"Examples: {examples.get('status', 'unknown')} ({examples.get('count', 0)} examples)")
        
        print("\nCore Functionality:")
        for feature in functionality.get('core_functionality', []):
            print(f"  {feature}")
        print()
        
        # Documentation Coverage
        print("📚 DOCUMENTATION COVERAGE")
        print("-" * 50)
        docs = self.report_data.get('documentation', {})
        print(f"Documentation Files: {docs.get('documentation_files', 0)}")
        
        if docs.get('documentation_topics'):
            print("\nAvailable Topics:")
            for topic in docs['documentation_topics']:
                print(f"  • {topic}")
        
        if docs.get('coverage_areas'):
            print("\nCoverage Areas:")
            for area, status in docs['coverage_areas'].items():
                print(f"  {status} {area}")
        print()
        
        # Completed Features
        print("✅ COMPLETED FEATURES")
        print("-" * 50)
        for feature in maturity.get('completed_features', []):
            print(f"• {feature}")
        print()
        
        # Readiness Metrics
        print("📈 READINESS METRICS")
        print("-" * 50)
        for metric, value in maturity.get('readiness_metrics', {}).items():
            print(f"• {metric}: {value}")
        print()
        
        # Next Steps
        print("🎯 RECOMMENDED NEXT STEPS")
        print("-" * 50)
        self._suggest_next_steps()
        print()
        
        print("=" * 70)
        print("Report complete! For more details, see individual documentation files.")
        print("=" * 70)
    
    def _suggest_next_steps(self):
        """Suggest next development steps based on current progress."""
        maturity = self.report_data.get('maturity', {})
        functionality = self.report_data.get('functionality', {})
        docs = self.report_data.get('documentation', {})
        
        suggestions = []
        
        # Check if we need web interface
        code_stats = self.report_data.get('code_structure', {})
        if 'ui' not in code_stats.get('components', {}):
            suggestions.append("1. Develop web user interface (UI components)")
        
        # Check if we need API endpoints
        if 'api' not in code_stats.get('components', {}):
            suggestions.append("2. Implement REST API endpoints")
        
        # Check if we need database integration
        suggestions.append("3. Add database integration for data persistence")
        
        # Check if we need more advanced features
        suggestions.append("4. Implement problem-solving algorithms")
        suggestions.append("5. Add team collaboration features")
        suggestions.append("6. Create reporting and analytics dashboard")
        
        # Security and deployment
        suggestions.append("7. Implement authentication and authorization")
        suggestions.append("8. Set up CI/CD pipeline")
        suggestions.append("9. Prepare deployment configuration")
        suggestions.append("10. Add integration tests and end-to-end testing")
        
        for suggestion in suggestions:
            print(f"  {suggestion}")
    
    def run_analysis(self):
        """Run the complete analysis and generate report."""
        self.logger.info("Starting project progress analysis...")
        
        self.analyze_code_structure()
        self.test_functionality()
        self.analyze_documentation()
        self.analyze_project_maturity()
        
        self.generate_report()
        
        self.logger.info("Progress analysis completed!")


def main():
    """Main function to run the progress analysis."""
    analyzer = ProjectAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()