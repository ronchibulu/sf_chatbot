"""Tests for user registration - Story 1.3"""
import pytest
from pathlib import Path


class TestRegistrationConfiguration:
    """Tests for Story 1.3: User Registration"""
    
    def test_registration_page_exists(self):
        """AC: Verify registration page exists."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        # Check both possible locations
        page_file = frontend_dir / "src" / "app" / "(auth)" / "register" / "page.tsx"
        if not page_file.exists():
            page_file = frontend_dir / "src" / "app" / "register" / "page.tsx"
        assert page_file.exists(), f"Registration page should exist at src/app/(auth)/register/page.tsx or src/app/register/page.tsx"
    
    def test_register_form_component_exists(self):
        """AC: Verify register form component exists."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        form_file = frontend_dir / "src" / "features" / "auth" / "components" / "register-form.tsx"
        assert form_file.exists(), "Register form component should exist"
        
        # Read with UTF-8 encoding
        content = form_file.read_text(encoding='utf-8')
        assert "RegisterForm" in content
        assert "zod" in content.lower() or "z." in content
    
    def test_auth_hooks_exist(self):
        """AC: Verify auth hooks exist."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        hooks_file = frontend_dir / "src" / "features" / "auth" / "hooks" / "use-auth.ts"
        assert hooks_file.exists(), "Auth hooks should exist"
        
        content = hooks_file.read_text()
        assert "signUp" in content
        assert "useAuth" in content
    
    def test_auth_types_exist(self):
        """Verify auth types are defined."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        types_file = frontend_dir / "src" / "features" / "auth" / "types" / "index.ts"
        assert types_file.exists(), "Auth types should exist"
    
    def test_dashboard_exists(self):
        """Verify dashboard page exists (redirect target)."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        dashboard_file = frontend_dir / "src" / "app" / "dashboard" / "page.tsx"
        assert dashboard_file.exists(), "Dashboard page should exist"
    
    def test_better_auth_client_installed(self):
        """AC: Verify better-auth/react is installed."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        package_json = frontend_dir / "package.json"
        
        assert package_json.exists()
        content = package_json.read_text()
        assert "better-auth" in content
    
    def test_zod_installed(self):
        """AC: Verify zod is installed for validation."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        package_json = frontend_dir / "package.json"
        
        content = package_json.read_text()
        assert "zod" in content
    
    def test_root_page_redirects(self):
        """Verify root page has auth redirect logic to /register."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        page_file = frontend_dir / "src" / "app" / "page.tsx"
        
        content = page_file.read_text()
        assert "getSession" in content
        assert "redirect" in content
        assert "/register" in content, "Root should redirect to /register for new users"
    
    def test_register_form_validation(self):
        """AC 3,4,5: Verify form has client-side validation."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        form_file = frontend_dir / "src" / "features" / "auth" / "components" / "register-form.tsx"
        
        content = form_file.read_text(encoding='utf-8')
        
        # Check for validation
        assert "email" in content.lower()
        assert "password" in content.lower()
        
        # Check for validation messages
        assert "Invalid" in content or "email" in content.lower()
        assert "8" in content or "min" in content.lower()  # Password min length
    
    def test_better_auth_route_handler(self):
        """AC 2: Verify BetterAuth sign-up endpoint is configured."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        route_file = frontend_dir / "src" / "app" / "api" / "auth" / "[...all]" / "route.ts"
        
        assert route_file.exists(), "BetterAuth route should exist"
        content = route_file.read_text()
        assert "better-auth" in content.lower() or "Auth" in content
    
    def test_register_form_has_error_display(self):
        """AC 2: Verify error messages are displayed in form."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        form_file = frontend_dir / "src" / "features" / "auth" / "components" / "register-form.tsx"
        
        content = form_file.read_text(encoding='utf-8')
        
        # Check error is displayed
        assert "error" in content.lower()
    
    def test_register_form_has_success_message(self):
        """AC 1: Verify success message is shown after registration."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        form_file = frontend_dir / "src" / "features" / "auth" / "components" / "register-form.tsx"
        
        content = form_file.read_text(encoding='utf-8')
        
        # Check success message/alert is shown
        assert "success" in content.lower() or "alert" in content.lower() or "toast" in content.lower()
    
    def test_auth_url_consistency(self):
        """Verify auth URLs are consistent between client and server."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        
        # Check auth-client.ts uses correct default
        client_file = frontend_dir / "src" / "lib" / "auth-client.ts"
        client_content = client_file.read_text()
        
        # Should default to 3000, not 3001
        assert "localhost:3000" in client_content, "auth-client should default to port 3000"
    
    def test_login_link_exists(self):
        """AC 5: Verify link to login page from register page."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        page_file = frontend_dir / "src" / "app" / "(auth)" / "register" / "page.tsx"
        
        content = page_file.read_text()
        assert "/login" in content, "Register page should have link to login"
