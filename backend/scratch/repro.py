import sys
sys.path.append('c:/Users/office/Documents/Final_year_project/backend')
import asyncio
from app.services.pipeline import run_text_pipeline

async def test():
    try:
        # This matches the call in text_router.py
        result, _ = await run_text_pipeline(
            user_email="test@example.com",
            text="This is a test sentence that is long enough to be valid.",
            mode="deep",
            include_highlights=True
        )
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
