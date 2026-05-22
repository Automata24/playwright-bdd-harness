class LoginPage:
    def __init__(self, page):
        self.page = page
        
        # Locators using the standard data-test attributes
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def navigate(self):
        """Navigates to the Swag Labs login page."""
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username, password):
        """Fills out the login form and clicks submit."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
