import os
import sys
import unittest

# Ensure the package directory is on the Python path so tests can import it
PACKAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../packages"))
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)

from authlibps.helpers import (
    get_supported_providers,
    get_provider_requirements,
    validate_oauth_config,
)
from authlibps.constants import PROVIDER_CONFIGS

class TestSupportedProviders(unittest.TestCase):
    def test_supported_providers_list(self):
        expected = sorted(PROVIDER_CONFIGS.keys())
        self.assertEqual(get_supported_providers(), expected)

class TestProviderRequirements(unittest.TestCase):
    def test_get_provider_requirements_matches_constants(self):
        for provider, cfg in PROVIDER_CONFIGS.items():
            req = get_provider_requirements(provider)
            self.assertEqual(req['provider_type'], cfg['type'])
            self.assertEqual(req['required_parameters'], cfg['required'])
            self.assertEqual(req['optional_parameters'], cfg.get('optional', set()))
            self.assertEqual(req['defaults'], cfg.get('defaults', {}))
            self.assertEqual(req['recommended_scope'], cfg.get('recommended_scope', ''))
            self.assertEqual(req['notes'], cfg.get('notes', ''))

class TestValidateOAuthConfig(unittest.TestCase):
    def test_validate_oauth_config_minimal_valid(self):
        for provider, cfg in PROVIDER_CONFIGS.items():
            minimal = {param: 'value' for param in cfg['required']}
            result = validate_oauth_config(provider, minimal)
            self.assertTrue(result.valid, provider)
            self.assertEqual(result.missing_required, [], provider)
            self.assertEqual(result.provider_type, cfg['type'])

if __name__ == '__main__':
    unittest.main()
