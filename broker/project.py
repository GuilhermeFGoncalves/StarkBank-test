import starkbank
from django.conf import settings

def get_project() -> starkbank.Project:
    """Builds the Stark Bank Project user used to authenticate every SDK call."""
    
    return starkbank.Project(
        environment=settings.STARKBANK_ENVIRONMENT,
        id=settings.STARKBANK_PROJECT_ID,
        private_key=settings.STARKBANK_PRIVATE_KEY,
    )
