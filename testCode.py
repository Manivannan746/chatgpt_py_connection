from google.adk.agents import Agent
from google.adk.tools import ToolContext


def get_monthly_savings(salary: float, expenses: float, tool:ToolContext) -> float:
    """
    Calculates the remaining savings after monthly expenses.

    Args:
        salary: The total monthly income (e.g., 100000).
        expenses: The total monthly spending.
    """
    return salary - expenses

finance_assistant = Agent(
    name="financial_assistance_ai",
    model="gemini-2.5-flash",
    description="Financial assistance AI to help finance needs",
    instruction="""You are a friendly assistant. Help me to manage monthly expense.
    1, Greet the user by analyzing local time from web
    2, Get the user name and account no from the user""",
    tools=[get_monthly_savings]
)

# This is the variable the ADK loader looks for
root_agent = finance_assistant

from google.adk.agents import Agent
from google.adk.tools import ToolContext

model = "gemini-2.5-flash-lite"

# --- PRODUCT CATALOG ---
PRODUCTS = {
    "laptop_001": {"name": "MacBook Pro 14", "price": 199900, "stock": 15},
    "phone_001": {"name": "iPhone 15 Pro", "price": 134900, "stock": 25},
    "tablet_001": {"name": "iPad Air", "price": 59900, "stock": 30},
    "watch_001": {"name": "Apple Watch Series 9", "price": 41900, "stock": 20},
    "headphones_001": {"name": "AirPods Pro", "price": 24900, "stock": 50}
}

# --- CUSTOM TOOLS ---
def get_customer_details(tool_context: ToolContext):
    """Fetches customer information from runtime context."""
    return {
        "name": getattr(tool_context.session, 'name', 'Guest User'),
        "email": getattr(tool_context.session, 'email', 'guest@example.com'),
        "mobile": getattr(tool_context.session, 'mobile', '+1-555-0000'),
        "address": getattr(tool_context.session, 'address', 'Address not provided')
    }

def get_product_catalog(tool_context: ToolContext):
    """Returns available products with prices and stock."""
    return PRODUCTS

def get_product_details(product_id: str, tool_context: ToolContext):
    """Get specific product details by ID."""
    return PRODUCTS.get(product_id, {"error": "Product not found"})

def calculate_total(items: str, tool_context: ToolContext):
    """Calculate total price for cart items. Items should be JSON string of cart items."""
    import json
    try:
        cart_items = json.loads(items)
        total = 0
        for item in cart_items:
            product = PRODUCTS.get(item["product_id"])
            if product:
                total += product["price"] * item["quantity"]
        return {"total": total, "formatted": f"₹{total:,}"}
    except:
        return {"error": "Invalid cart items format"}

# --- SUB AGENTS ---
catalog_agent = Agent(
    name="catalog_specialist",
    model=model,
    description="Product search and inventory specialist",
    instruction="""Help users find products from our catalog:
    - MacBook Pro 14: ₹1,99,900
    - iPhone 15 Pro: ₹1,34,900
    - iPad Air: ₹59,900
    - Apple Watch Series 9: ₹41,900
    - AirPods Pro: ₹24,900
    
    Check stock levels and suggest alternatives if needed.""",
    tools=[get_product_catalog, get_product_details]
)

checkout_agent = Agent(
    name="checkout_specialist",
    model=model,
    description="Payment and order processing specialist",
    instruction="""Handle checkout process:
    1. Calculate totals with taxes
    2. Confirm shipping address
    3. Process payment
    4. Generate order confirmation
    
    Default shipping address: 123 Main St, City, State 12345
    Ask user to confirm or provide new address.""",
    tools=[calculate_total, get_customer_details]
)

tracking_agent = Agent(
    name="tracking_specialist",
    model=model,
    description="Order tracking and delivery specialist",
    instruction="Provide shipping updates and delivery estimates. Standard delivery: 3-5 business days."
)

# --- MAIN AGENT ---
root_agent = Agent(
    name="ecommerce_assistant",
    model=model,
    description="Complete eCommerce shopping assistant",
    tools=[
        get_customer_details,
        get_product_catalog,
        get_product_details,
        calculate_total
    ],
    sub_agents= [catalog_agent, checkout_agent, tracking_agent],
    instruction="""You are a helpful eCommerce assistant. Available products:
    
    📱 Electronics:
    - MacBook Pro 14: ₹1,99,900 (15 in stock)
    - iPhone 15 Pro: ₹1,34,900 (25 in stock)
    - iPad Air: ₹59,900 (30 in stock)
    - Apple Watch Series 9: ₹41,900 (20 in stock)
    - AirPods Pro: ₹24,900 (50 in stock)
    
    🛒 Shopping Flow:
    1. Greet user and and get the user details from get_customer_details() dynamically
    2. Show the products and Help find specific items
    3. Calculate totals for cart
    4. Confirm shipping address: 123 Main St, City, State 12345
    5. Process checkout
    6. Mention about completion of checkout
    
    Use tools to fetch real product data and customer details."""
)
