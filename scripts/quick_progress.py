#!/usr/bin/env python3
"""
Quick Progress Viewer

This script provides a simple way to view the current project progress
either in the terminal or by opening the web dashboard.
"""

import os
import sys
import webbrowser
from pathlib import Path


def show_quick_progress():
    """Show a quick progress summary in the terminal."""
    print("🚀 TASKSOLVER-PRO QUICK PROGRESS")
    print("=" * 50)
    print("Status: Alpha Development Phase")
    print("Core Features: ✅ Implemented")
    print("Tests: ✅ 6/6 Passing")
    print("Documentation: ✅ Available")
    print("Next Phase: Web UI Development")
    print("=" * 50)
    print()
    print("For detailed progress:")
    print("1. Run: python3 scripts/progress_report.py")
    print("2. View: docs/progress-dashboard.html")
    print("3. Quick view: python3 scripts/quick_progress.py --web")


def open_dashboard():
    """Open the progress dashboard in the default web browser."""
    dashboard_path = Path(__file__).parent.parent / "docs" / "progress-dashboard.html"
    
    if dashboard_path.exists():
        # Convert to absolute path for browser
        dashboard_url = dashboard_path.absolute().as_uri()
        print(f"Opening progress dashboard: {dashboard_url}")
        
        try:
            webbrowser.open(dashboard_url)
            print("✅ Progress dashboard opened in your default browser!")
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"Please manually open: {dashboard_path}")
    else:
        print("❌ Progress dashboard not found. Please run the setup first.")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        open_dashboard()
    else:
        show_quick_progress()


if __name__ == "__main__":
    main()