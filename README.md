# 🛍️ TataCliq Product Scraper

A Streamlit web application for scraping product data from TataCliq.com. Upload an Excel file with product URLs or IDs and get comprehensive product information including pricing, images, specifications, reviews, and more.

## Features

- 📊 **Bulk Scraping**: Process multiple products simultaneously
- 🚀 **Concurrent Processing**: Configurable worker threads (1-16) for faster scraping
- 📥 **Excel Import/Export**: Upload input Excel, download results as Excel
- 🔍 **Comprehensive Data**: Extracts 100+ data points per product including:
  - Product details (title, description, brand)
  - Pricing (MRP, selling price, discount)
  - Images (all product images)
  - Specifications and classifications
  - Size guides with measurements
  - Customer reviews and ratings
  - Seller information
  - Manufacturing details
  - Return policies
  - A+ Content
  - And much more!

## Live Demo

🌐 **Deployed on Streamlit Cloud**: [Your App URL will appear here after deployment]

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tatacliq-scraper.git
cd tatacliq-scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

5. Open your browser and navigate to `http://localhost:8501`

## Usage

1. **Prepare Input File**: Create an Excel file with product URLs or IDs
   - Column name: `url` (for full URLs) or `id` (for product IDs)
   - Optional: Add `s.no` column for tracking

   Example:
   ```
   | s.no | url                                                                                      |
   |------|------------------------------------------------------------------------------------------|
   | 1    | https://www.tatacliq.com/woodland-green-beige-cotton-shirt/p-mp000000026178350         |
   | 2    | https://www.tatacliq.com/another-product/p-mp000000012345678                            |
   ```

2. **Upload File**: Click "Upload Excel file" and select your input file

3. **Configure Settings**: 
   - Adjust the number of concurrent workers (default: 8)
   - More workers = faster, but may cause rate limiting

4. **Start Scraping**: Click "🚀 Start Scraping"

5. **Download Results**: Once complete, click "📥 Download Results (Excel)"

## Input Format

Your Excel file should contain one of the following:

- **Full URL** in a column named `url`:
  ```
  https://www.tatacliq.com/product-name/p-PRODUCTID
  ```

- **Product ID** in a column named `id`:
  ```
  mp000000026178350
  ```

## Output Data

The scraper extracts the following information:

### Basic Information
- Product title, brand, color, description
- Product code and listing ID
- Category hierarchy (breadcrumbs)

### Pricing
- MRP (Maximum Retail Price)
- Selling Price
- Discount percentage

### Images
- All product images in high resolution

### Specifications
- Material, fit, pattern, sleeve type
- Dimensions and measurements
- Size guide with charts
- Available sizes

### Reviews & Ratings
- Average rating
- Number of ratings
- Number of reviews
- Customer voice (fitting feedback)

### Seller Information
- Seller name and address
- Manufacturer details
- Packer information

### Additional Details
- Return and refund policies
- Product composition
- A+ Content (enhanced descriptions)
- Brand information
- Care instructions

## Deploy to Streamlit Cloud

1. **Push to GitHub**:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. Your app will be live at: `https://yourusername-tatacliq-scraper-app-xxxxx.streamlit.app`

## Important Notes

⚠️ **Rate Limiting**: TataCliq may rate-limit requests if you scrape too aggressively. Start with fewer workers (4-8) and increase if needed.

⚠️ **Legal Compliance**: Ensure you comply with TataCliq's Terms of Service and robots.txt. This tool is for educational purposes.

⚠️ **Cookie Updates**: The scraper uses request headers with cookies. These may expire over time. Update the cookies in `app.py` if you encounter authentication issues.

## Troubleshooting

### Issue: "No data was scraped"
- Check if the product URLs/IDs are valid
- Verify your internet connection
- Try reducing the number of workers
- Update cookies in the code if they've expired

### Issue: Rate limiting errors
- Reduce the number of concurrent workers
- Add delays between requests
- Contact TataCliq if you need API access

### Issue: Missing data fields
- Some products may not have all fields
- The scraper handles missing data gracefully
- Check the progress log for specific errors

## Configuration

Edit `app.py` to customize:

- **Headers**: Update request headers and cookies (lines 16-28)
- **Timeout**: Adjust request timeout (default: 10-15 seconds)
- **Max Workers**: Change default concurrent workers
- **Output Format**: Modify the Excel output structure

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is provided for educational purposes only. Users are responsible for ensuring their use complies with TataCliq's Terms of Service and applicable laws. The developers assume no liability for misuse.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## Changelog

### Version 1.0.0 (2026-02-04)
- Initial release
- Concurrent scraping support
- Excel import/export
- Comprehensive data extraction
- Streamlit Cloud deployment ready

---

Made with ❤️ using Streamlit
