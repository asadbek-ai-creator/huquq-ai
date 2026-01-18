#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify UTF-8 encoding support for Karakalpak language
Test script to ensure proper character encoding
"""

import sys
import locale


def check_system_encoding():
    """Check system encoding settings"""
    print("=" * 60)
    print("System Encoding Check")
    print("=" * 60)

    # Python default encoding
    default_encoding = sys.getdefaultencoding()
    print(f"Python default encoding: {default_encoding}")
    assert default_encoding == "utf-8", "Python default encoding must be UTF-8"

    # File system encoding
    fs_encoding = sys.getfilesystemencoding()
    print(f"File system encoding: {fs_encoding}")

    # Locale encoding
    try:
        locale_encoding = locale.getpreferredencoding()
        print(f"Locale encoding: {locale_encoding}")
    except Exception as e:
        print(f"Could not get locale encoding: {e}")

    # Standard streams
    print(f"stdout encoding: {sys.stdout.encoding}")
    print(f"stderr encoding: {sys.stderr.encoding}")
    print(f"stdin encoding: {sys.stdin.encoding}")

    print()


def test_karakalpak_characters():
    """Test Karakalpak language characters"""
    print("=" * 60)
    print("Karakalpak Language Character Test")
    print("=" * 60)

    # Karakalpak alphabet special characters
    karakalpak_chars = "ǵ ń ı ú ó á"
    print(f"Special characters: {karakalpak_chars}")

    # Karakalpak legal terms
    terms = {
        "Nızam": "Law",
        "Statiya": "Article",
        "Jinayat": "Crime",
        "Jaza": "Punishment",
        "Jinayat Kodeksi": "Criminal Code",
        "Puqaralıq Kodeksi": "Civil Code",
        "Soraw beriwshi": "User/Questioner",
        "Juwap": "Answer",
        "Izlew": "Search",
        "Jinayattıń awır túri": "Heavy crime"
    }

    print("\nLegal terminology in Karakalpak:")
    for kaa, eng in terms.items():
        try:
            print(f"  {kaa:25} -> {eng}")
            # Verify encoding/decoding
            encoded = kaa.encode('utf-8')
            decoded = encoded.decode('utf-8')
            assert kaa == decoded, f"Encoding mismatch for: {kaa}"
        except Exception as e:
            print(f"  ERROR with '{kaa}': {e}")
            raise

    print()


def test_file_operations():
    """Test file read/write with UTF-8"""
    print("=" * 60)
    print("File Operations Test")
    print("=" * 60)

    import tempfile
    import os

    test_text = """
    # Karakalpak Legal Terms
    Nızam - Huqıqlıq nızam
    Statiya - Huqıqlıq statiya
    Jinayat - Jinayat isi
    Jaza - Huqıqlıq jaza
    """

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            delete=False,
            suffix='.txt'
        ) as f:
            f.write(test_text)
            temp_path = f.name

        print(f"Created temp file: {temp_path}")

        # Read back
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verify
        assert content == test_text, "File content mismatch"
        print("✓ File write/read successful")

        # Cleanup
        os.unlink(temp_path)
        print("✓ Cleanup successful")

    except Exception as e:
        print(f"✗ File operations failed: {e}")
        raise

    print()


def test_yaml_config():
    """Test YAML configuration with Karakalpak text"""
    print("=" * 60)
    print("YAML Configuration Test")
    print("=" * 60)

    try:
        import yaml

        config_sample = {
            'terminology': {
                'karakalpak': {
                    'nizam': 'Nızam',
                    'statiya': 'Statiya',
                    'jinayat': 'Jinayat',
                    'jaza': 'Jaza'
                }
            }
        }

        # Test YAML dump
        yaml_str = yaml.dump(config_sample, allow_unicode=True)
        print("YAML output:")
        print(yaml_str)

        # Test YAML load
        loaded = yaml.safe_load(yaml_str)
        assert loaded == config_sample, "YAML roundtrip failed"
        print("✓ YAML encoding/decoding successful")

    except ImportError:
        print("⚠ PyYAML not installed, skipping YAML test")
    except Exception as e:
        print(f"✗ YAML test failed: {e}")
        raise

    print()


def main():
    """Run all encoding tests"""
    # Handle Windows console encoding
    if sys.platform == 'win32':
        try:
            # Try to set UTF-8 encoding for Windows console
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleCP(65001)
            kernel32.SetConsoleOutputCP(65001)
        except:
            pass

    print("\n")
    print("=" * 60)
    print(" " * 10 + "huquqAI UTF-8 Encoding Verification")
    print("=" * 60)
    print()

    try:
        check_system_encoding()
        test_karakalpak_characters()
        test_file_operations()
        test_yaml_config()

        print("=" * 60)
        print("[PASS] ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("Your system is properly configured for Karakalpak language!")
        print("UTF-8 encoding is working correctly.")
        print()

        # Display system info
        print("System Information:")
        print(f"  Python version: {sys.version.split()[0]}")
        print(f"  Platform: {sys.platform}")
        print(f"  Default encoding: {sys.getdefaultencoding()}")
        print()

        return 0

    except AssertionError as e:
        print("\n" + "=" * 60)
        print("[FAIL] TEST FAILED")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\nPlease ensure your system supports UTF-8 encoding.")
        print("\nFix for Windows:")
        print("  1. Run: chcp 65001")
        print("  2. Set: PYTHONIOENCODING=utf-8")
        print("  3. Restart your terminal")
        print("\nFix for Linux/Mac:")
        print("  export LC_ALL=en_US.UTF-8")
        print("  export LANG=en_US.UTF-8")
        print()
        return 1

    except Exception as e:
        print("\n" + "=" * 60)
        print("[ERROR] UNEXPECTED ERROR")
        print("=" * 60)
        print(f"\nError: {e}")
        print(f"\nError type: {type(e).__name__}")

        if "codec" in str(e).lower() or "encoding" in str(e).lower():
            print("\nThis appears to be an encoding issue.")
            print("\nQuick fix for Windows:")
            print("  Run this command before running the script:")
            print("  chcp 65001 && set PYTHONIOENCODING=utf-8")
            print()

        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
