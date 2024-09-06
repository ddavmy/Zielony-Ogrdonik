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

async def get_gardenfields_without_watered_image(page, img_src):
    divs_without_watered_background_image = await page.evaluate(f"""
        (imgSrc) => {{
            const divs = document.querySelectorAll('div.gardenfield');
            const matchingDivs = [];

            divs.forEach(div => {{
                const imgElement = div.querySelector('img.wasser');
                if (imgElement && imgElement.src === imgSrc) {{
                    matchingDivs.push(div.id);
                }}
            }});

            return matchingDivs;
        }}
    """, img_src)

    return divs_without_watered_background_image