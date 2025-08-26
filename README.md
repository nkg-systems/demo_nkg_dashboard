# Sales Intelligence Dashboard

> **Modern SMB Sales Dashboard with AI-Inspired Dark Theme**

A sophisticated, real-time sales analytics dashboard built with Streamlit, featuring a modern dark theme with blue/violet accents. This dashboard transforms your Google Sheets data into powerful, actionable insights for modern businesses.

![Dashboard Preview](https://img.shields.io/badge/Status-Production_Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎨 **Modern Design**
- **Dark Theme**: Professional dark background with blue/violet gradient accents
- **Interactive UI**: Hover effects, smooth transitions, and modern typography
- **Responsive Layout**: Optimized for desktop and mobile viewing
- **Custom Styling**: Hand-crafted CSS with Inter font family

### 📊 **Advanced Analytics**
- **Real-time Data Processing**: Automatic updates every 15 minutes
- **Interactive Filtering**: Date ranges, channels, owners, and status filters
- **Smart Visualizations**: Revenue trends, lead funnels, and conversion analytics
- **KPI Metrics**: Leads, conversion rates, revenue, ROAS, CAC, and more

### 🔮 **AI-Powered Insights**
- **Predictive Analytics**: Conversion trend analysis
- **Performance Optimization**: Intelligent caching and data loading
- **Smart Segmentation**: Advanced filtering and data categorization
- **Automated Reporting**: CSV export functionality

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Sheets with published CSV access
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/demo_nkg_dashboard.git
   cd demo_nkg_dashboard
   ```

2. **Set up virtual environment**
   ```bash
   cd demo-dashboard
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your data source**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   # Required: your published-to-web CSV link
   CSV_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/pub?gid=0&single=true&output=csv"
   
   # Optional: Access control
   ACCESS_CODE = "your-secret-code"
   
   # Optional: Branding
   COMPANY_NAME = "Your Company"
   LOGO_URL = "https://your-cdn.com/logo.png"
   ```

5. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 📈 Data Format

Your Google Sheets should have the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `date` | Date | Lead creation date |
| `channel` | Text | Marketing channel (e.g., "Google Ads", "Facebook") |
| `campaign` | Text | Campaign name |
| `lead_name` | Text | Lead's name |
| `lead_email` | Email | Lead's email address |
| `lead_phone` | Text | Lead's phone number |
| `status` | Text | Lead status ("New", "Qualified", "Won", "Lost") |
| `revenue` | Number | Deal value (for "Won" status) |
| `cost` | Number | Marketing cost |
| `owner` | Text | Sales rep or team member |

### Google Sheets Setup
1. Create a Google Sheet with your sales data
2. Go to **File → Share → Publish to web**
3. Select your sheet and choose **CSV** format
4. Copy the published URL to your `secrets.toml`

## 🎨 UI Components

### Header Section
- **AI-themed gradient header** with animated background
- **Feature badges** highlighting real-time capabilities
- **Modern typography** with professional styling

### Control Panel (Sidebar)
- **Data source configuration** with connection status
- **AI features showcase** with capability highlights
- **Performance metrics** (when data is loaded)

### Analytics Section
- **KPI Cards**: Interactive metrics with hover effects
- **Revenue Trends**: Time-series visualization with gradient fills
- **Lead Funnel**: Color-coded status distribution
- **Channel Performance**: Horizontal bar chart with conversion rates

### Data Table
- **Responsive table** with sorting and filtering
- **Export functionality** for filtered data
- **Modern styling** with dark theme consistency

## ⚙️ Configuration

### Theme Customization
The dashboard uses CSS custom properties for easy theming:

```css
:root {
    --primary-violet: #8B5CF6;
    --primary-blue: #3B82F6;
    --accent-cyan: #06B6D4;
    --bg-primary: #0B0F1A;
    --bg-secondary: #11172A;
    --text-primary: #E6EAF3;
    /* ... more variables */
}
```

### Streamlit Configuration
The `demo-dashboard/.streamlit/config.toml` contains:
- Dark theme base colors
- Custom accent colors (violet/blue)
- Typography and layout settings

## 🔧 Development

### Project Structure
```
demo_nkg_dashboard/
├── demo-dashboard/
│   ├── .streamlit/
│   │   ├── config.toml      # Streamlit theme config
│   │   └── secrets.toml     # Secret credentials
│   ├── .venv/               # Virtual environment
│   ├── app.py              # Main dashboard application
│   └── requirements.txt    # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
└── README.md              # This file
```

### Key Files
- **`app.py`**: Main Streamlit application with AI-themed styling
- **`config.toml`**: Streamlit theme configuration
- **`secrets.toml`**: Secure configuration (not in Git)
- **`requirements.txt`**: Python package dependencies

### Dependencies
- **streamlit**: Web app framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **requests**: HTTP client for data fetching
- **python-dateutil**: Date parsing utilities

## 🎯 Features in Detail

### Real-time Data Processing
- **Automatic refresh**: Data updates every 15 minutes
- **Smart caching**: Optimized performance with `@st.cache_data`
- **Error handling**: Graceful handling of data source issues

### Interactive Filtering
- **Date range picker**: Custom time period selection
- **Multi-select filters**: Channels, owners, and status options
- **Dynamic updates**: Real-time chart and metric updates

### Advanced Visualizations
- **Plotly charts**: Interactive, responsive visualizations
- **Custom color schemes**: Consistent with dark theme
- **Hover effects**: Detailed data on mouse interaction
- **Responsive design**: Adapts to different screen sizes

## 🚀 Deployment

### Streamlit Cloud
1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy from your fork
4. Add secrets in the Streamlit Cloud dashboard

### Docker (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY demo-dashboard/ .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Credits

**Developed by**: NKG-Systems + NathanGr33n  
**Theme**: Modern AI-inspired dark design  
**Framework**: Streamlit with custom CSS styling  

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/demo_nkg_dashboard/issues) page
2. Create a new issue with detailed information
3. Include screenshots and error messages when possible

## 🔮 Future Enhancements

- [ ] **Machine Learning Integration**: Predictive lead scoring
- [ ] **Advanced Filters**: Custom date ranges and complex queries
- [ ] **Email Reports**: Automated scheduled reports
- [ ] **Multi-language Support**: Internationalization
- [ ] **Advanced Security**: Role-based access control
- [ ] **API Integration**: Direct CRM connections

---

**Made with ❤️ by NKG-Systems**

*Transform your sales data into actionable insights with AI-powered analytics*
