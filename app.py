import streamlit as st
import json
import requests
import concurrent.futures
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict
from html import unescape
from copy import deepcopy
import io
import time

# Page config
st.set_page_config(
    page_title="TataCliq Product Scraper",
    page_icon="🛍️",
    layout="wide"
)

# Headers for requests
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'mode': 'no-cors',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

# Size guide helpers
def format_size_header(raw_dim, unit=None):
    if unit:
        unit = "Inches" if unit.lower() == "in" else unit
        return f"{raw_dim} ( {unit} )"
    return raw_dim

def get_size_guide(ID_from_input, sizeGuideId, headers):
    params = {
        'isPwa': 'true',
        'sizeGuideId': sizeGuideId,
        'rootCategory': 'Clothing',
    }
    response = requests.get(
        f'https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/{ID_from_input.upper()}/sizeGuideChart',
        params=params,
        headers=headers,
        timeout=10
    )
    try:
        json_size = response.json()
    except Exception:
        return OrderedDict()
    
    tabular = json_size.get('sizeGuideTabularWsData')
    if not tabular:
        return OrderedDict()
    
    unit_data = OrderedDict()
    main_size = []
    for size_map in tabular.get('unitList', []):
        unit = size_map.get('displaytext')
        if not unit:
            continue
        unit_data.setdefault(unit, OrderedDict())
        for size_name in size_map.get('sizeGuideList', []):
            size = size_name.get('dimensionSize')
            if not size:
                continue
            if size not in main_size:
                main_size.append(size)
            for size_value in size_name.get('dimensionList', []):
                dim = size_value.get('dimension')
                val = size_value.get('dimensionValue')
                if not dim or val is None:
                    continue
                unit_data[unit].setdefault(dim, []).append(val)
    
    final_output = OrderedDict()
    if main_size:
        final_output["Brand Size"] = main_size
    
    dims = set(unit_data.get('Cm', {})) | set(unit_data.get('In', {}))
    for dim in dims:
        cm_vals = unit_data.get('Cm', {}).get(dim)
        in_vals = unit_data.get('In', {}).get(dim)
        if cm_vals == in_vals:
            final_output[format_size_header(dim)] = cm_vals
        else:
            if cm_vals:
                final_output[format_size_header(dim, "Cm")] = cm_vals
            if in_vals:
                final_output[format_size_header(dim, "In")] = in_vals
    
    if json_size.get('imageURL'):
        final_output['measurement_image'] = json_size['imageURL']
    
    return final_output

def clean_html(text):
    return BeautifulSoup(unescape(text), "html.parser").get_text(". ", strip=True)

def get_data(data, headers, progress_callback=None):
    try:
        # Extract ID from data - try multiple approaches
        ID_from_input = ""
        
        # Look through all keys in the data dictionary
        for key, value in data.items():
            if value and isinstance(value, str):
                # Check if it's a URL
                if "tatacliq.com" in value and "/p-" in value:
                    ID_from_input = value.split("/p-")[-1]
                    break
                # Check if it looks like a product ID
                elif value.startswith("mp") or value.startswith("MP"):
                    ID_from_input = value
                    break
        
        # If still no ID found, return error
        if not ID_from_input:
            if progress_callback:
                progress_callback(f"❌ No valid URL or product ID found in row. Columns: {list(data.keys())}")
            return None
        
        # Clean up the ID
        ID_from_input = ID_from_input.strip()
        newid = ID_from_input.upper()
        
        product_url = f"https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/productDetails/{ID_from_input.upper()}?isPwa=true&isMDE=true&isDynamicVar=true"
        res = requests.get(product_url, headers=headers, timeout=15)
        
        try:
            json_data = res.json()
        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ JSON failed for ID: {ID_from_input}")
            return None
        
        nettemp = {}
        variant_found = False
        
        if json_data.get("variantOptions"):
            for i in json_data["variantOptions"]:
                sizelink = i.get("sizelink")
                colorlink = i.get("colorlink")
                if not sizelink:
                    continue
                if sizelink.get("productCode") == newid:
                    data.update({
                        "product_url": "https://www.tatacliq.com" + sizelink.get("url", ""),
                        "product_code": sizelink.get("productCode"),
                        "Product_size": sizelink.get("size"),
                        "color": colorlink.get("color") if colorlink else None,
                        "color_hex": colorlink.get("colorHexCode") if colorlink else None
                    })
                    variant_found = True
                    break
        
        if not variant_found:
            data["product_url"] = "https://www.tatacliq.com" + json_data.get("seo", {}).get("alternateURL", "")
            data["product_code"] = ID_from_input
        
        # Basic product info
        data["productTitle"] = json_data.get("productTitle")
        data["brandName"] = json_data.get("brandName")
        data["productColor"] = json_data.get("productColor")
        data["productDescription"] = json_data.get("productDescription")
        data["productListingId"] = json_data.get("productListingId")
        data["rootCategory"] = json_data.get("rootCategory")
        data["styleNote"] = json_data.get("styleNote")
        
        nettemp["usisd"] = json_data.get("winningUssID")
        nettemp["brandURL"] = json_data.get("brandURL", "").split("c-")[-1].upper()
        nettemp["categoryL4Code"] = json_data.get("categoryL4Code")
        
        # Category hierarchy
        if json_data.get("categoryHierarchy"):
            for i, cat in enumerate(json_data["categoryHierarchy"]):
                data[f"Breadcrums_{i+1}"] = cat["category_name"]
        
        # Pricing
        if json_data.get("mrpPrice"):
            data["MRP"] = json_data["mrpPrice"]["value"]
        if json_data.get("winningSellerPrice"):
            data["Price"] = json_data["winningSellerPrice"]["value"]
        if json_data.get("discount"):
            data["Discount"] = json_data["discount"]
        
        # Details
        if json_data.get("details"):
            for i in json_data["details"]:
                data[i["key"]] = i["value"]
        
        # Images
        if json_data.get("galleryImagesList"):
            img = []
            for g in json_data["galleryImagesList"]:
                for k in g["galleryImages"]:
                    if k["key"] == "superZoom":
                        img.append("https:" + k["value"])
            for i, im in enumerate(img):
                data[f"image_{i+1}"] = im
        
        # Manufacturing details
        if json_data.get("mfgDetails"):
            for k, v in json_data["mfgDetails"].items():
                if isinstance(v, list):
                    data[k] = v[0]["value"]
                else:
                    data[k] = v
        
        # Return details
        if json_data.get("knowMore"):
            for index, i in enumerate(json_data.get("knowMore"), start=1):
                data[f"Return_Details_{index}"] = i.get('knowMoreItem')
        
        # Classifications
        if json_data.get("classifications"):
            for classification in json_data.get("classifications", []):
                for spec in classification.get("specifications", []):
                    if spec.get("key") and spec.get("value"):
                        data[spec["key"]] = spec["value"]
        
        # Seller info
        if json_data.get('winningSellerName'):
            data['Seller_name'] = json_data.get('winningSellerName')
        if json_data.get('winningSellerAddress'):
            data['Seller_address'] = json_data.get('winningSellerAddress')
        if json_data.get('brandInfo'):
            data['brandInfo'] = json_data.get('brandInfo')
        
        # Jewelry classifications
        for block in json_data.get("fineJewelleryClassificationList", []):
            for item in block.get("value", {}).get("classificationListJwlry", []):
                if item.get("key"):
                    data[item["key"]] = ", ".join(
                        item.get("value", {}).get("classificationListValueJwlry", [])
                    )
        
        # Refund info
        for idx, item in enumerate(json_data.get("returnAndRefund", []), start=1):
            if item.get("refundReturnItem"):
                data[f"refundReturnInfo_{idx}"] = item["refundReturnItem"]
        
        # Details section
        for item in json_data.get("detailsSection", []):
            if item.get("key") and item.get("value"):
                data[item["key"]] = item["value"]
        
        # Ingredients
        for item in json_data.get("otherIngredients", []):
            data['composition'] = item.get('value')
        
        # Classification list
        for section in json_data.get("classificationList", []):
            section_key = section.get("key")
            value_block = section.get("value", {})
            if "classificationList" in value_block:
                for item in value_block.get("classificationList", []):
                    if item.get("key") and item.get("value"):
                        data[item["key"].strip()] = item["value"].strip()
            elif "classificationValues" in value_block:
                data[section_key] = ", ".join(v.strip() for v in value_block.get("classificationValues", []))
        
        # Ratings
        data['average_ratings'] = json_data.get('averageRating', '')
        data['ratingCount'] = json_data.get('ratingCount', '')
        data['numberOfReviews'] = json_data.get('numberOfReviews', '')
        
        # Available sizes
        available_sizes = []
        for group in json_data.get("variantGroup", []):
            for s in group.get("sizeOptions", []):
                if s.get("size") and s["size"] not in available_sizes:
                    available_sizes.append(s["size"])
        if available_sizes:
            data["Available Size"] = available_sizes
        
        # Size guide
        try:
            if json_data.get("sizeGuideId"):
                data.update(get_size_guide(ID_from_input, json_data["sizeGuideId"], headers))
        except Exception:
            pass
        
        # Brand size from variants
        if not data.get("Brand Size"):
            for variant in json_data.get("variantOptions", []):
                if variant.get("dynamicVariantlink", {}).get("selected"):
                    data["Color"] = variant.get("colorlink", {}).get("color")
                    data["Purity"] = variant.get("dynamicVariantlink", {}).get("dynamicVariantValue")
                    data["Brand Size"] = variant.get("dynamicVariantlink", {}).get("sizeLink", {}).get("brandSize")
                    break
        
        # Customer voice
        try:
            cutomer_voice_response = requests.get(
                f'https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/{ID_from_input.upper()}/customerVoice',
                headers=headers,
                timeout=10
            )
            response_json = cutomer_voice_response.json()
            for item in response_json.get("customerVoiceData", []):
                data[item["text"]] = item["value"]
        except Exception:
            pass
        
        # Beauty extra info
        set_info = json_data.get("setInformation")
        if set_info:
            for item in set_info.get("values", []):
                data[item["key"]] = item["value"]
        
        what_else = json_data.get("whatElseYouNeedtoKnow", [])
        for item in what_else:
            key = item.get("key")
            value = item.get("value")
            if key and value:
                data[key] = value
        
        ingredient_details = json_data.get("ingredientDetails", [])
        for item in ingredient_details:
            main_key = item.get("key")
            values = item.get("values", [])
            if main_key and values:
                ingredients = [v.get("key") for v in values if v.get("key")]
                if ingredients:
                    data[main_key] = ", ".join(ingredients)
        
        primary_ingredients = json_data.get("primaryIngredients", [])
        for item in primary_ingredients:
            key = item.get("key")
            value = item.get("value")
            if key and value:
                data[key] = value
        
        short_story = json_data.get("shortStorySmall", [])
        features = [
            item.get("key")
            for item in sorted(short_story, key=lambda x: x.get("order", 0))
            if item.get("key")
        ]
        if features:
            data["additional_features"] = ", ".join(features)
        
        # Manufacturer and packer
        try:
            brand_id = json_data.get('brandURL', '').split('c-')[1]
            category_hierarchy = json_data.get("categoryHierarchy", [])
            if category_hierarchy:
                last_category_id = category_hierarchy[-1].get("category_id")
                
                manufacturer_params = {
                    'category': last_category_id.upper(),
                    'brand': brand_id.upper(),
                }
                
                manufacturer_response = requests.get(
                    'https://www.tatacliq.com/marketplacewebservices/v2/mpl/products/manufacturingdetails',
                    params=manufacturer_params,
                    headers=headers,
                    timeout=10
                )
                manufacturer_json = manufacturer_response.json()
                
                for item in manufacturer_json.get("manufacturer", []):
                    if item.get("value"):
                        if not data.get('manufacturer'):
                            data["manufacturer"] = item["value"]
                            break
                
                for item in manufacturer_json.get("packer", []):
                    if item.get("value"):
                        if not data.get('packer'):
                            data["packer"] = item["value"]
                            break
        except Exception:
            pass
        
        # A+ Content
        count = 1
        for item in json_data.get("APlusContent", {}).get("productContent", []):
            text_list = item.get("value", {}).get("textList")
            if text_list:
                cleaned_text = " ".join(clean_html(t) for t in text_list if t)
                if cleaned_text:
                    data[f"aplus_information_{count}"] = cleaned_text
                    count += 1
        
        data.update(nettemp)
        
        if progress_callback:
            progress_callback(f"✅ Completed: {data.get('s.no', ID_from_input)}")
        
        return deepcopy(data)
        
    except Exception as error:
        if progress_callback:
            progress_callback(f"❌ Error in ID {ID_from_input}: {str(error)}")
        return None

# Streamlit UI
def main():
    st.title("🛍️ TataCliq Product Scraper")
    st.markdown("Upload an Excel file with product URLs or IDs to scrape product data from TataCliq.")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        max_workers = st.slider("Number of concurrent workers", 1, 16, 8)
        st.info("Higher workers = faster scraping, but may cause rate limiting")
        
        st.markdown("---")
        st.markdown("### 📋 Input Format")
        st.markdown("""
        Your Excel file should have either:
        - A column named `url` with full product URLs
        - A column named `id` with product IDs
        - Optional: `s.no` column for tracking
        """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            df_raw = pd.read_excel(uploaded_file)
            df = df_raw.to_dict("records")
            st.success(f"✅ Loaded {len(df)} products from file")
            
            # Check if there's any URL or ID in the data
            has_valid_data = False
            first_row = df[0] if len(df) > 0 else {}
            
            for value in first_row.values():
                if value and isinstance(value, str):
                    if "tatacliq.com" in str(value) or str(value).startswith("mp") or str(value).startswith("MP"):
                        has_valid_data = True
                        break
            
            if not has_valid_data:
                st.error(f"❌ No TataCliq URLs or product IDs found. Please check your Excel file.")
                st.info("💡 Your Excel should have a column with TataCliq URLs (e.g., https://www.tatacliq.com/.../p-mp000000012345678)")
                st.stop()
            
            # Show preview
            with st.expander("📊 Preview input data"):
                st.dataframe(df_raw.head())
            
            # Scrape button
            if st.button("🚀 Start Scraping", type="primary"):
                all_data = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                log_area = st.empty()
                logs = []
                
                def update_progress(msg):
                    logs.append(msg)
                    log_area.text_area("📝 Progress Log", "\n".join(logs[-10:]), height=200)
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {executor.submit(get_data, item, HEADERS, update_progress): item for item in df}
                    
                    completed = 0
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        if result:
                            all_data.append(result)
                        completed += 1
                        progress = completed / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f"Progress: {completed}/{len(df)} products")
                
                if all_data:
                    result_df = pd.DataFrame(all_data)
                    
                    st.success(f"✅ Successfully scraped {len(all_data)} products!")
                    
                    # Show results
                    with st.expander("📊 Preview results"):
                        st.dataframe(result_df.head(10))
                    
                    # Download button
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False, sheet_name='Products')
                    
                    st.download_button(
                        label="📥 Download Results (Excel)",
                        data=output.getvalue(),
                        file_name=f"tatacliq_products_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error("❌ No data was scraped. Please check the logs above.")
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    else:
        # Show sample format
        st.info("👆 Upload an Excel file to get started")
        with st.expander("📄 Sample Input Format"):
            sample_df = pd.DataFrame({
                's.no': [1, 2],
                'url': [
                    'https://www.tatacliq.com/woodland-green-beige-cotton-regular-fit-checks-shirt/p-mp000000026178350',
                    'https://www.tatacliq.com/some-product/p-mp000000012345678'
                ]
            })
            st.dataframe(sample_df)

if __name__ == "__main__":
    main()
