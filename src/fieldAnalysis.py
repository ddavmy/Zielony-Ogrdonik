async def get_gardenfields_with_image(page, empty_url):
    divs_with_empty_background_image = await page.evaluate(f"""
        (backgroundImageUrl) => {{
            const gardenfields = Array.from(document.querySelectorAll('div.gardenfield'));
            const result = gardenfields.filter(div => {{
                const childDivs = div.querySelectorAll('div');
                return Array.from(childDivs).some(child => {{
                    const style = window.getComputedStyle(child);
                    return style.backgroundImage.includes(backgroundImageUrl);
                }});
            }});
            return result.map(div => div.id);
        }}
    """, empty_url)
    return divs_with_empty_background_image

async def get_gardenfields_with_different_image(page, target_image_fragment):
    divs_with_different_background_image = await page.evaluate(f"""
        (targetImageFragment) => {{
            const gardenfields = Array.from(document.querySelectorAll('div.gardenfield'));
            const result = gardenfields.filter(div => {{
                const childDivs = div.querySelectorAll('div');
                return Array.from(childDivs).some(child => {{
                    const style = window.getComputedStyle(child);
                    const backgroundImageUrl = style.backgroundImage;
                    const imageFragment = backgroundImageUrl.split('/produkte/')[1]?.replace('")', '');
                    return imageFragment && imageFragment !== targetImageFragment;
                }});
            }});
            return result.map(div => div.id);
        }}
    """, target_image_fragment)
    return divs_with_different_background_image
