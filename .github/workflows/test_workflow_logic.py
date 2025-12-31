#!/usr/bin/env python3
"""
Test script to simulate the workflow logic locally.
This script demonstrates how the ADD and DELETE commands would work.

Note: This is for testing purposes only. The actual workflow runs in GitHub Actions.
"""

import re
import json

def parse_command(comment_body):
    """Parse ADD or DELETE command from comment"""
    add_pattern = r'ADD\s+(\S+)\s+(\S+)'
    delete_pattern = r'DELETE\s+(\S+)\s+(\S+)'
    
    add_match = re.search(add_pattern, comment_body)
    delete_match = re.search(delete_pattern, comment_body)
    
    if add_match:
        return 'ADD', add_match.group(1), add_match.group(2)
    elif delete_match:
        return 'DELETE', delete_match.group(1), delete_match.group(2)
    else:
        return None, None, None

def test_parse_commands():
    """Test the command parsing logic"""
    test_cases = [
        ("ADD friends https://example.com/feed.xml", 'ADD', 'friends', 'https://example.com/feed.xml'),
        ("DELETE friends https://example.com/feed.xml", 'DELETE', 'friends', 'https://example.com/feed.xml'),
        ("Please ADD tech https://tech.example.com/rss", 'ADD', 'tech', 'https://tech.example.com/rss'),
        ("Can you DELETE blog https://blog.example.com/atom.xml", 'DELETE', 'blog', 'https://blog.example.com/atom.xml'),
        ("Just a regular comment", None, None, None),
        ("ADD section1 https://example.com/feed1.xml\nADD section2 https://example.com/feed2.xml", 'ADD', 'section1', 'https://example.com/feed1.xml'),
    ]
    
    print("Testing command parsing:")
    print("-" * 80)
    
    for comment, expected_cmd, expected_section, expected_url in test_cases:
        cmd, section, url = parse_command(comment)
        status = "✓" if (cmd, section, url) == (expected_cmd, expected_section, expected_url) else "✗"
        print(f"{status} Comment: {comment[:50]}...")
        print(f"  Parsed: {cmd} {section} {url}")
        print(f"  Expected: {expected_cmd} {expected_section} {expected_url}")
        print()

def simulate_add_operation():
    """Simulate ADD operation"""
    print("\nSimulating ADD operation:")
    print("-" * 80)
    
    # Simulate existing gist content
    current_data = [
        "https://example1.com/feed.xml",
        "https://example2.com/rss.xml"
    ]
    
    print(f"Current data: {json.dumps(current_data, indent=2)}")
    
    # Add new URL
    new_url = "https://example3.com/atom.xml"
    if new_url not in current_data:
        current_data.append(new_url)
        print(f"\n✅ Successfully added: {new_url}")
    else:
        print(f"\nℹ️ URL already exists: {new_url}")
    
    print(f"\nUpdated data: {json.dumps(current_data, indent=2)}")

def simulate_delete_operation():
    """Simulate DELETE operation"""
    print("\nSimulating DELETE operation:")
    print("-" * 80)
    
    # Simulate existing gist content
    current_data = [
        "https://example1.com/feed.xml",
        "https://example2.com/rss.xml",
        "https://example3.com/atom.xml"
    ]
    
    print(f"Current data: {json.dumps(current_data, indent=2)}")
    
    # Remove URL
    remove_url = "https://example2.com/rss.xml"
    if remove_url in current_data:
        current_data.remove(remove_url)
        print(f"\n✅ Successfully removed: {remove_url}")
    else:
        print(f"\nℹ️ URL not found: {remove_url}")
    
    print(f"\nUpdated data: {json.dumps(current_data, indent=2)}")

if __name__ == "__main__":
    print("=" * 80)
    print("Workflow Logic Test Script")
    print("=" * 80)
    
    test_parse_commands()
    simulate_add_operation()
    simulate_delete_operation()
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)
