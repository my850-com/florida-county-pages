#!/usr/bin/env python3
"""Generate 67 county HTML pages from Google Sheet data."""

import json
import os
import subprocess
import sys
from datetime import datetime

def get_sheet_data():
    """Pull county SEO data from Google Sheet."""
    sheet_id = "1d_UzZrIs4oO5Z3Nshc_UO4Fcorbimmm6rKovIyybdcg"
    range_name = "'FLP SEO List'!A2:P68"
    
    result = subprocess.run(
        ["gog", "sheets", "get", sheet_id, range_name, "--json"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"Error fetching sheet: {result.stderr}")
        return None
    
    data = json.loads(result.stdout)
    return data.get("values", [])

def slugify(county_name):
    """Convert county name to URL-friendly slug."""
    return county_name.lower().replace(" ", "-").replace(".", "").replace("'", "")

def generate_html(county_data, template):
    """Generate HTML for a single county."""
    # Map sheet columns to template variables
    County = county_data[0] if len(county_data) > 0 else ""
    Filings_Weekly = county_data[1] if len(county_data) > 1 else ""
    Major_Cities = county_data[3] if len(county_data) > 3 else ""
    Cities_Count = county_data[4] if len(county_data) > 4 else ""
    Market_Highlight = county_data[5] if len(county_data) > 5 else ""
    Intro_Paragraph = county_data[6] if len(county_data) > 6 else ""
    FAQ_1 = county_data[7] if len(county_data) > 7 else ""
    FAQ_1_Answer = county_data[8] if len(county_data) > 8 else ""
    FAQ_2 = county_data[9] if len(county_data) > 9 else ""
    FAQ_2_Answer = county_data[10] if len(county_data) > 10 else ""
    Nearby_1 = county_data[11] if len(county_data) > 11 else ""
    Nearby_2 = county_data[12] if len(county_data) > 12 else ""
    Nearby_3 = county_data[13] if len(county_data) > 13 else ""
    
    # Build FAQ section
    faq_section = ""
    if FAQ_1:
        faq_section += f'<div class="faq-item"><div class="faq-question">{FAQ_1}</div><div class="faq-answer">{FAQ_1_Answer}</div></div>'
    if FAQ_2:
        faq_section += f'<div class="faq-item"><div class="faq-question">{FAQ_2}</div><div class="faq-answer">{FAQ_2_Answer}</div></div>'
    
    # Format nearby counties for display
    nearby_links = ""
    for nearby in [Nearby_1, Nearby_2, Nearby_3]:
        if nearby:
            nearby_slug = slugify(nearby)
            nearby_links += f'                <a href="./{nearby_slug}.html" style="color: #003366; text-decoration: none; margin: 0 15px; font-weight: bold;">{nearby} County &rarr;</a>\n'
    
    # Format first 3 cities for display
    cities_list = [c.strip() for c in Major_Cities.split(",") if c.strip()][:12]
    cities_display = ", ".join(cities_list[:3]) if cities_list else Major_Cities[:50]
    
    # Build cities grid HTML
    cities_grid = ''.join(f'<div class="city-tag">{c}</div>' for c in cities_list[:12])
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{County} County Lis Pendens Filings | Florida Lis Pendens Data</title>
    <meta name="description" content="{County} County generates {Filings_Weekly} weekly Lis Pendens filings. Find pre-foreclosure properties in {County}. Data from {County} County Clerk of Courts.">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, Helvetica, sans-serif; line-height: 1.6; color: #333; background: #fff; }}
        .header {{ background: #003366; padding: 20px; text-align: center; }}
        .header-logo {{ color: #fff; font-size: 24px; font-weight: bold; letter-spacing: 2px; }}
        .header-tagline {{ color: #ccc; font-size: 12px; margin-top: 5px; letter-spacing: 1px; }}
        .back-link {{ color: #fff; text-decoration: none; font-size: 14px; display: inline-block; margin-top: 15px; padding: 8px 20px; border: 1px solid #fff; border-radius: 25px; }}
        .back-link:hover {{ background: rgba(255,255,255,0.1); }}
        .hero {{ background: linear-gradient(135deg, #003366 0%, #0066cc 100%); color: #fff; padding: 60px 20px; text-align: center; }}
        .hero h1 {{ font-size: 42px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }}
        .hero-subtitle {{ font-size: 20px; margin-bottom: 30px; color: #e0e0e0; }}
        .hero-stats {{ background: rgba(255,255,255,0.1); display: inline-block; padding: 30px 50px; border-radius: 10px; margin: 20px 0; }}
        .stat-number {{ font-size: 56px; font-weight: bold; color: #FFD700; }}
        .stat-label {{ font-size: 16px; text-transform: uppercase; letter-spacing: 1px; }}
        .btn {{ display: inline-block; padding: 15px 35px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 16px; margin: 10px; transition: all 0.3s ease; }}
        .btn-primary {{ background: #FFD700; color: #003366; }}
        .btn-primary:hover {{ background: #e6c200; transform: translateY(-2px); }}
        .btn-secondary {{ background: transparent; color: #fff; border: 2px solid #fff; }}
        .btn-secondary:hover {{ background: rgba(255,255,255,0.1); }}
        .content {{ max-width: 900px; margin: 0 auto; padding: 60px 20px; }}
        .section {{ margin-bottom: 50px; }}
        .section h2 {{ color: #003366; font-size: 28px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 3px solid #FFD700; display: inline-block; }}
        .section p {{ font-size: 16px; line-height: 1.8; color: #555; margin-bottom: 15px; }}
        .faq-item {{ background: #f8f9fa; border-left: 4px solid #003366; padding: 20px; margin-bottom: 20px; border-radius: 0 8px 8px 0; }}
        .faq-question {{ font-weight: bold; color: #003366; font-size: 18px; margin-bottom: 10px; }}
        .faq-answer {{ color: #666; }}
        .cta-box {{ background: linear-gradient(135deg, #003366 0%, #004080 100%); color: #fff; padding: 50px; border-radius: 10px; text-align: center; margin: 40px 0; }}
        .cta-box h3 {{ font-size: 28px; margin-bottom: 15px; }}
        .cta-box p {{ color: #e0e0e0; margin-bottom: 25px; font-size: 16px; }}
        .cities-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0; }}
        .city-tag {{ background: #f0f4f8; padding: 10px 15px; border-radius: 20px; text-align: center; color: #003366; font-weight: 500; }}
        .footer {{ background: #003366; color: #fff; padding: 40px 20px; text-align: center; }}
        .footer-logo {{ font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
        .footer-tagline {{ font-size: 12px; color: #ccc; margin-bottom: 20px; }}
        .footer-links {{ margin: 20px 0; }}
        .footer-links a {{ color: #fff; text-decoration: none; margin: 0 15px; font-size: 14px; }}
        .footer-contact {{ margin-top: 20px; font-size: 14px; color: #ccc; }}
        @media (max-width: 768px) {{ .hero h1 {{ font-size: 28px; }} .stat-number {{ font-size: 36px; }} .btn {{ display: block; margin: 10px auto; max-width: 280px; }} }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-logo">FLORIDA LIS PENDENS</div>
        <div class="header-tagline">A MY850.COM COMPANY</div>
        <a href="https://floridalispendens.com" class="back-link">&larr; Back to Main Site</a>
    </header>
    
    <section class="hero">
        <h1>{County} County</h1>
        <div class="hero-subtitle">Lis Pendens Filings</div>
        <div class="hero-stats">
            <div class="stat-number">{Filings_Weekly}</div>
            <div class="stat-label">Weekly Filings</div>
        </div>
        <div>
            <a href="https://floridalispendens.com/subscribe" class="btn btn-primary">Get Weekly Alerts</a>
            <a href="#about" class="btn btn-secondary">Learn More</a>
        </div>
    </section>
    
    <main class="content">
        <section class="section" id="about">
            <h2>About {County} County Lis Pendens</h2>
            <p>{Intro_Paragraph}</p>
        </section>
        
        <section class="section">
            <h2>Major Cities in {County} County</h2>
            <p>This data covers {Cities_Count} cities including {cities_display}.</p>
            <div class="cities-grid">{cities_grid}</div>
        </section>
        
        <section class="section" id="faq">
            <h2>Frequently Asked Questions</h2>
            {faq_section}
        </section>
        
        <div class="cta-box">
            <h3>Get {County} County Alerts</h3>
            <p>Subscribe to receive weekly Lis Pendens filing data for {County} County.</p>
            <a href="https://floridalispendens.com/subscribe" class="btn btn-primary">View Pricing</a>
        </div>
        
        <section class="section">
            <h2>Nearby Counties</h2>
            <p>Also providing Lis Pendens data for these neighboring counties:</p>
            <p style="text-align: center; margin-top: 20px;">\n{nearby_links}</p>
        </section>
        
        <section class="section">
            <h2>Why {County} County?</h2>
            <p>{Market_Highlight}</p>
        </section>
    </main>
    
    <footer class="footer">
        <div class="footer-logo">FLORIDA LIS PENDENS</div>
        <div class="footer-tagline">A MY850.COM COMPANY</div>
        <div class="footer-links">
            <a href="https://floridalispendens.com">Home</a>
            <a href="https://floridalispendens.com/subscribe">Services</a>
        </div>
        <div class="footer-contact">
            (850) 998-8500\n4507 Furling #106 Destin, FL 32541
        </div>
    </footer>
</body>
</html>'''
    
    return html

def main():
    """Generate all 67 county pages."""
    print("Fetching county data from Google Sheet...")
    counties = get_sheet_data()
    
    if not counties:
        print("Failed to fetch data")
        return 1
    
    print(f"Found {len(counties)} counties")
    
    # Generate HTML for each county
    for county_data in counties:
        if not county_data or not county_data[0]:
            continue
        
        county_name = county_data[0]
        slug = slugify(county_name)
        filename = f"{slug}.html"
        
        print(f"Generating {filename}...", end=" ")
        
        html = generate_html(county_data, None)
        
        with open(filename, "w") as f:
            f.write(html)
        
        print("OK")
    
    # Generate index.html
    with open("index.html", "w") as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=https://floridalispendens.com">
    <title>Florida County Lis Pendens Data</title>
</head>
<body>
    <p>Redirecting to <a href="https://floridalispendens.com">Florida Lis Pendens</a>...</p>
</body>
</html>''')
    
    print(f"\n✅ Generated {len([c for c in counties if c and c[0]])} pages + index.html")
    return 0

if __name__ == "__main__":
    sys.exit(main())
