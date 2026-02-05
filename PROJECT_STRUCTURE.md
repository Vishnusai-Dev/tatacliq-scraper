# 📁 Project Structure

```
tatacliq-scraper/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── sample_input.xlsx          # Sample input file with example URLs
├── create_sample.py           # Script to generate sample input file
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
│
├── README.md                  # Full documentation
├── QUICKSTART.md              # Quick start guide
├── DEPLOYMENT.md              # Deployment instructions
└── PROJECT_STRUCTURE.md       # This file
```

## File Descriptions

### Core Files

#### `app.py` (Main Application)
The heart of the application. Contains:
- Streamlit UI code
- Web scraping logic
- Data extraction functions
- Size guide parsing
- Customer review extraction
- Manufacturer details fetching
- A+ content extraction
- Concurrent processing with ThreadPoolExecutor

**Key Functions:**
- `get_data()`: Main scraping function for each product
- `get_size_guide()`: Extracts size guide information
- `format_size_header()`: Formats size dimensions
- `clean_html()`: Cleans HTML content
- `main()`: Streamlit UI and app logic

#### `requirements.txt`
Python package dependencies:
```
streamlit==1.31.0      # Web framework
pandas==2.1.4          # Data manipulation
openpyxl==3.1.2        # Excel file handling
requests==2.31.0       # HTTP requests
beautifulsoup4==4.12.3 # HTML parsing
lxml==5.1.0            # XML/HTML parser
```

### Configuration Files

#### `.streamlit/config.toml`
Streamlit app configuration:
- Theme colors
- Upload size limits (200 MB)
- Security settings
- CORS configuration

#### `.gitignore`
Excludes from version control:
- Python cache files
- Virtual environments
- IDE settings
- Output Excel files (except sample)
- OS-specific files
- Logs and environment variables

### Documentation Files

#### `README.md`
Comprehensive documentation including:
- Feature overview
- Installation instructions
- Usage guide
- Input/output formats
- Deployment guide
- Troubleshooting
- Configuration options

#### `QUICKSTART.md`
Quick start guide for:
- Local setup (5 minutes)
- Streamlit Cloud deployment
- Creating input files
- Common issues and solutions

#### `DEPLOYMENT.md`
Detailed deployment instructions:
- GitHub repository setup
- Streamlit Cloud deployment
- Custom domain configuration
- Environment variables
- Security best practices
- Troubleshooting deployment issues

#### `PROJECT_STRUCTURE.md`
This file - project organization reference

### Sample Files

#### `sample_input.xlsx`
Example input file with:
- Sample product URLs
- Proper column format (`s.no`, `url`)
- Ready to use for testing

#### `create_sample.py`
Python script to generate `sample_input.xlsx`
- Creates properly formatted Excel file
- Includes sample TataCliq URLs
- Useful for regenerating sample data

### Legal

#### `LICENSE`
MIT License - permissive open source license

## Data Flow

```
Input Excel File
    ↓
Upload to Streamlit
    ↓
Parse URLs/IDs
    ↓
Concurrent Scraping (ThreadPoolExecutor)
    ↓
Extract Product Data
    ├── Basic Info (title, brand, price)
    ├── Images (all product images)
    ├── Specifications
    ├── Size Guide
    ├── Customer Reviews
    ├── Seller Info
    ├── Manufacturing Details
    └── A+ Content
    ↓
Combine All Data
    ↓
Export to Excel
    ↓
Download Results
```

## Key Features Implementation

### 1. Concurrent Scraping
- Uses `concurrent.futures.ThreadPoolExecutor`
- Configurable workers (1-16)
- Progress tracking with callbacks

### 2. Comprehensive Data Extraction
- 100+ data points per product
- Handles missing data gracefully
- Parses complex nested JSON

### 3. Size Guide Parsing
- Extracts measurements in multiple units (cm/inches)
- Creates structured size charts
- Includes measurement images

### 4. Excel I/O
- Reads Excel input with pandas
- Writes formatted Excel output
- Preserves data types and formatting

### 5. Error Handling
- Try-catch blocks for each section
- Continues on partial failures
- Logs all errors to UI

### 6. UI/UX
- Progress bars
- Real-time log updates
- Preview of input/output data
- One-click download

## Customization Points

### Adding New Data Fields
Edit `app.py` → `get_data()` function:
```python
# Add new extraction logic
if json_data.get("newField"):
    data["newField"] = json_data["newField"]
```

### Changing Request Headers
Edit `app.py` → `HEADERS` dictionary:
```python
HEADERS = {
    'user-agent': 'Your User Agent',
    'cookie': 'your-cookies',
    # ... other headers
}
```

### Adjusting Timeouts
Edit timeout parameters in requests:
```python
requests.get(url, timeout=15)  # Change from 15 to desired value
```

### UI Customization
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#FF6B6B"  # Change colors
backgroundColor="#FFFFFF"
```

## Dependencies Explained

| Package | Purpose | Used For |
|---------|---------|----------|
| streamlit | Web framework | UI, file upload, progress bars |
| pandas | Data manipulation | Excel I/O, DataFrame operations |
| openpyxl | Excel engine | Reading/writing .xlsx files |
| requests | HTTP library | API calls, web scraping |
| beautifulsoup4 | HTML parser | Cleaning HTML content |
| lxml | Parser backend | Fast HTML/XML parsing |

## Environment Requirements

- Python 3.8+
- 200 MB+ RAM (depends on batch size)
- Internet connection (for scraping)
- Modern browser (for Streamlit UI)

## Future Enhancements

Potential features to add:
- [ ] Database storage option
- [ ] API rate limiting with retries
- [ ] Image download functionality
- [ ] CSV export option
- [ ] Scheduled scraping
- [ ] Email notifications
- [ ] Data validation rules
- [ ] Duplicate detection
- [ ] Price tracking over time

## Maintenance

### Regular Updates
1. Update dependencies monthly:
   ```bash
   pip install --upgrade -r requirements.txt
   pip freeze > requirements.txt
   ```

2. Update cookies when expired:
   - Check browser network tab
   - Copy fresh cookies
   - Update `HEADERS` in `app.py`

3. Test with sample products weekly

### Monitoring
- Check Streamlit Cloud logs
- Monitor error rates
- Track scraping success rate
- Watch for API changes

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Pandas Docs**: https://pandas.pydata.org
- **Requests Docs**: https://requests.readthedocs.io
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-04  
**Maintainer**: Your Name
