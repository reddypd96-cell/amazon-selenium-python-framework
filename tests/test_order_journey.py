
from pages.home_page import HomePage
from config import config
from utils.logger import get_logger

log = get_logger(__name__)


def test_full_order_journey(driver):
    # open Amazon, click Sign in
    home = HomePage(driver).load()
    login = home.go_to_sign_in()

    # enter mobile number and password
    login.enter_mobile_number(config.MOBILE_NUMBER)
    home = login.enter_password(config.PASSWORD)
    log.info("Signed in successfully")

    # search for iphone
    results = home.search_for(config.SEARCH_TERM)
    assert results.results_count() > 0, "No search results found"

    # adding the first result to cart direct
    
    product = results.add_first_result_to_cart()
    log.info("Added item to cart")

    # click on the cart icon
    cart = product.go_to_cart()
    assert cart.is_item_in_cart(), "Item was not added to cart"

    # proceed to buy
    checkout = cart.proceed_to_buy()

    # choose Cash on Delivery
    checkout.select_cash_on_delivery()
    log.info("Selected Cash on Delivery")

    # place the order
    orders_page = checkout.place_order()

    if orders_page is None:
        log.info(
            
        )
        return

    log.info("Order placed")

    # Returns & Orders
    orders_page = orders_page.go_to_orders()
    assert orders_page.has_orders(), "No orders found on the orders page"

    # track package
    orders_page.track_first_order()
    status = orders_page.get_status()
    log.info(f"Order status: {status}")
    assert status
