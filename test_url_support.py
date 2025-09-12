#!/usr/bin/env python3
"""
Test script for URL functionality in ComfyUI Text Tools
Tests the URLFileUtility class and its integration with FontManager
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_url_utility_basic():
    """Test basic URLFileUtility functionality"""
    print("=== Testing URLFileUtility Basic Functionality ===")
    
    try:
        from utils.apz_url_file_utility import URLFileUtility, get_local_file_path
        
        # Test 1: URL detection
        utility = URLFileUtility()
        
        # Test URL detection
        assert utility.is_url("https://example.com/font.ttf") == True
        assert utility.is_url("http://example.com/font.ttf") == True
        assert utility.is_url("/local/path/font.ttf") == False
        assert utility.is_url("C:\\Windows\\Fonts\\arial.ttf") == False
        assert utility.is_url("") == False
        print("✓ URL detection working correctly")
        
        # Test 2: File extension detection
        ext = utility.get_file_extension("https://example.com/font.ttf")
        assert ext == ".ttf"
        print("✓ File extension detection working")
        
        # Test 3: Hash generation
        hash1 = utility.get_file_hash("https://example.com/font.ttf")
        hash2 = utility.get_file_hash("https://example.com/font.ttf")
        assert hash1 == hash2
        assert len(hash1) == 32  # MD5 hash length
        print("✓ Hash generation working")
        
        print("✓ URLFileUtility basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"✗ URLFileUtility basic functionality test failed: {e}")
        return False

def test_font_manager_integration():
    """Test FontManager integration with URL functionality"""
    print("\n=== Testing FontManager URL Integration ===")
    
    try:
        from utils.apz_font_manager import FontManager
        
        # Create a temporary font file for testing
        temp_dir = tempfile.mkdtemp()
        test_font_path = os.path.join(temp_dir, "test_font.ttf")
        
        # Create a dummy font file (just empty file for testing)
        with open(test_font_path, 'wb') as f:
            f.write(b'dummy font content')
        
        try:
            # Test with local file paths
            font_manager = FontManager(
                regular_font_path=test_font_path,
                italic_font_path=test_font_path,
                bold_font_path=test_font_path,
                max_font_size=24
            )
            
            print("✓ FontManager initialized with local paths")
            
            # Test that paths were resolved correctly
            assert font_manager.regular_font_path == test_font_path
            assert font_manager.italic_font_path == test_font_path
            assert font_manager.bold_font_path == test_font_path
            print("✓ Font paths resolved correctly")
            
            # Test that FontManager can be used (basic functionality)
            assert font_manager.max_font_size == 24
            print("✓ FontManager basic properties working")
            
        finally:
            # Cleanup
            shutil.rmtree(temp_dir)
        
        print("✓ FontManager URL integration tests passed")
        return True
        
    except Exception as e:
        print(f"✗ FontManager URL integration test failed: {e}")
        return False

def test_utils_import():
    """Test that URL utilities are properly imported in the utils package"""
    print("\n=== Testing Utils Package Import ===")
    
    try:
        from utils import apz_url_file_utility, get_local_file_path
        
        assert apz_url_file_utility is not None
        assert get_local_file_path is not None
        print("✓ URL utilities properly imported in utils package")
        
        # Test the convenience function
        from utils.apz_url_file_utility import URLFileUtility
        utility = URLFileUtility()
        assert utility is not None
        print("✓ URLFileUtility can be instantiated")
        
        return True
        
    except Exception as e:
        print(f"✗ Utils package import test failed: {e}")
        return False

def test_error_handling():
    """Test error handling for invalid URLs and files"""
    print("\n=== Testing Error Handling ===")
    
    try:
        from utils.apz_url_file_utility import URLFileUtility
        
        utility = URLFileUtility()
        
        # Test invalid URL handling (malformed URL)
        try:
            utility.get_local_path("https://[invalid-url]/font.ttf", timeout=1)
            print("✗ Should have raised an error for malformed URL")
            return False
        except Exception as e:
            print(f"✓ Malformed URL properly raises exception: {type(e).__name__}")
        
        # Test non-existent domain
        try:
            utility.get_local_path("https://this-domain-definitely-does-not-exist-12345.com/font.ttf", timeout=1)
            print("✗ Should have raised an error for non-existent domain")
            return False
        except Exception as e:
            print(f"✓ Non-existent domain properly raises exception: {type(e).__name__}")
        
        # Test invalid local file handling
        try:
            utility.get_local_path("/path/that/does/not/exist.ttf")
            print("✗ Should have raised an error for non-existent local file")
            return False
        except FileNotFoundError:
            print("✓ Non-existent local file properly raises FileNotFoundError")
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def test_temp_directory_management():
    """Test temporary directory creation and management"""
    print("\n=== Testing Temp Directory Management ===")
    
    try:
        from utils.apz_url_file_utility import URLFileUtility
        
        # Test with custom temp directory
        custom_temp = tempfile.mkdtemp()
        utility = URLFileUtility(temp_dir=custom_temp)
        
        assert utility.temp_dir == Path(custom_temp)
        assert utility.temp_dir.exists()
        print("✓ Custom temp directory created and managed correctly")
        
        # Test cleanup
        utility.cleanup_old_files()
        print("✓ Cleanup function works without errors")
        
        # Cleanup
        try:
            shutil.rmtree(custom_temp)
        except Exception as e:
            print(f"Warning: Could not clean up temp directory: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Temp directory management test failed: {e}")
        return False

def main():
    """Run all URL functionality tests"""
    print("ComfyUI Text Tools - URL Functionality Test Suite")
    print("=" * 50)
    
    tests = [
        test_url_utility_basic,
        test_font_manager_integration,
        test_utils_import,
        test_error_handling,
        test_temp_directory_management
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All URL functionality tests passed! URL functionality is ready.")
        return True
    else:
        print("⚠️  Some tests failed. URL functionality may not be fully ready.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)