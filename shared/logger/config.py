import logging
import structlog
from datetime import datetime

# Set up the file handler
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"logs/mcp_client_{timestamp}.log"

file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(logging.Formatter("%(message)s"))

# Basic logging config
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler],  # Send logs to file
)

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()                   # Render as JSON
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),          # Use stdlib logging
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)
