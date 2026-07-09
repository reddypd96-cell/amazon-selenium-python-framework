"""
End-to-end order journey on amazon.in:

Home -> Sign in -> Search "iphone" -> Add to cart -> Cart -> Proceed to buy
-> Choose Cash on Delivery -> Place order -> Orders page -> Track package

Credentials and the PLACE_REAL_ORDER switch come from config, which reads
them from a local .env file - nothing sensitive is hardcoded here.
"""

from pages.home_page import HomePage
from config import config
from utils.logger import get_logger

log = get_logger(__name__)


def test_full_order_journey(driver):
    # Step 1-2: open Amazon, hover over the greeting, click Sign in
    home = HomePage(driver).load()
    login = home.go_to_sign_in()

    # Step 3-4: enter mobile number and password
    login.enter_mobile_number(config.MOBILE_NUMBER)
    home = login.enter_password(config.PASSWORD)
    log.info("Signed in successfully")

    # Step 5: search for iphone
    results = home.search_for(config.SEARCH_TERM)
    assert results.results_count() > 0, "No search results found"

    # Step 6-7: add the first result to cart directly from the search
    # results page, dismissing the max-quantity popup if it shows up
    product = results.add_first_result_to_cart()
    log.info("Added item to cart")

    # Step 8: click the cart icon
    cart = product.go_to_cart()
    assert cart.is_item_in_cart(), "Item was not added to cart"

    # Step 9: proceed to buy
    checkout = cart.proceed_to_buy()

    # Step 10: choose Cash on Delivery
    checkout.select_cash_on_delivery()
    log.info("Selected Cash on Delivery")

    # Step 11: place the order (real, gated by PLACE_REAL_ORDER in .env)
    orders_page = checkout.place_order()

    if orders_page is None:
        log.info(
            "Stopped before placing a real order (PLACE_REAL_ORDER=false). "
            "Journey verified up to the final confirmation step."
        )
        return

    log.info("Order placed")

    # Step 12: Returns & Orders - clickable from the confirmation page,
    # the nav bar is present on every Amazon page
    orders_page = orders_page.go_to_orders()
    assert orders_page.has_orders(), "No orders found on the orders page"

    # Step 13: track package
    orders_page.track_first_order()
    status = orders_page.get_status()
    log.info(f"Order status: {status}")
    assert status
