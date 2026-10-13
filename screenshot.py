import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        # Launch chromium
        browser = await p.chromium.launch()
        page = await browser.new_page(device_scale_factor=2) # High resolution
        
        # Get absolute path to the HTML file
        file_path = os.path.abspath('diagram_viewer.html')
        file_url = f"file:///{file_path.replace(os.sep, '/')}"
        
        print(f"Loading {file_url}...")
        await page.goto(file_url)
        
        # Wait for mermaid to render the SVG
        await page.wait_for_selector('svg')
        await page.wait_for_timeout(1000) # Give it a second to finish styling
        
        # Target the mermaid div
        element = await page.query_selector('.mermaid')
        
        # Save directly to your artifacts folder so it shows up in the chat
        output_path = r"C:\Users\moham\.gemini\antigravity-ide\brain\71b23608-765c-4b98-b7a9-9c12eb01411a\flowchart.png"
        
        await element.screenshot(path=output_path)
        print(f"Saved perfect screenshot to {output_path}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
