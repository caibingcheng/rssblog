#!/usr/bin/env python3
"""
Test script to simulate the workflow logic locally.
This script demonstrates how the ADD and DELETE commands would work.

Note: This is for testing purposes only. The actual workflow runs in GitHub Actions.
"""

import re
import json

def should_trigger_workflow(comment_author, repository_owner, comment_body):
    """
    Simulate the workflow trigger condition.
    
    Returns True if the workflow should trigger, False otherwise.
    This matches the condition in manage-gist.yml:
      github.event.comment.user.login == github.repository_owner &&
      (contains(github.event.comment.body, 'ADD') || 
      contains(github.event.comment.body, 'DELETE'))
    """
    # Check if comment author is the repository owner
    if comment_author != repository_owner:
        return False
    
    # Check if comment contains ADD or DELETE command
    has_add = 'ADD' in comment_body
    has_delete = 'DELETE' in comment_body
    
    return has_add or has_delete

def parse_command(comment_body):
    """Parse ADD or DELETE command from comment.

    Returns a tuple of (command, section, url), or (None, None, None) if
    no valid command is found.
    """
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

def test_workflow_permission_check():
    """Test the workflow permission check logic"""
    repository_owner = "caibingcheng"
    
    test_cases = [
        # (comment_author, comment_body, should_trigger, description)
        ("caibingcheng", "ADD friends https://example.com/feed.xml", True, "Owner with ADD command"),
        ("caibingcheng", "DELETE friends https://example.com/feed.xml", True, "Owner with DELETE command"),
        ("caibingcheng", "Just a regular comment", False, "Owner without command"),
        ("other-user", "ADD friends https://example.com/feed.xml", False, "Non-owner with ADD command"),
        ("other-user", "DELETE friends https://example.com/feed.xml", False, "Non-owner with DELETE command"),
        ("other-user", "Just a regular comment", False, "Non-owner without command"),
        ("caibingcheng", "Please ADD tech https://tech.example.com/rss", True, "Owner with ADD in sentence"),
        ("random-user", "Can you DELETE blog https://blog.example.com/atom.xml", False, "Non-owner with DELETE in sentence"),
    ]
    
    print("\nTesting workflow permission check:")
    print("-" * 80)
    
    all_passed = True
    for author, body, expected, description in test_cases:
        result = should_trigger_workflow(author, repository_owner, body)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"{status} {description}")
        print(f"  Author: {author}, Expected: {expected}, Got: {result}")
        print()
    
    return all_passed

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
    
    # Test permission check first
    permission_test_passed = test_workflow_permission_check()
    
    # Test command parsing
    test_parse_commands()
    
    # Test operations
    simulate_add_operation()
    simulate_delete_operation()
    
    print("\n" + "=" * 80)
    if permission_test_passed:
        print("✅ All tests completed successfully!")
    else:
        print("❌ Some permission tests failed!")
    print("=" * 80)
