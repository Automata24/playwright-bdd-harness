class CheckoutPage:
    def __init__(self, page):
        self.page = page
        
        # Step 1: Your Information Locators
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        
        # Step 2: Overview Locators
        self.finish_button = page.locator("[data-test='finish']")
        
        # Step 3: Complete Locators
        self.complete_header = page.locator("[data-test='complete-header']")

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        """Fills out the user information form and continues."""
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        """Clicks finish on the order review page."""
        self.finish_button.click()

    def get_success_message(self) -> str:
        """Returns the final success confirmation text."""
        return self.complete_header.text_content()
