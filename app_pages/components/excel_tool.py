"""
Excel Tool Component - Batch insert screenshot files into Excel files
"""
import streamlit as st
import os
import time
import logging
import zipfile
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image as ExcelImage

# Try importing pandas and xlrd to support .xls format
try:
    import pandas as pd
    XLS_SUPPORT = True
except ImportError:
    XLS_SUPPORT = False
    pd = None

# ==================== Excel Tool Helper Classes ====================
# Supported image formats
SUPPORTED_IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}

# Default configuration
DEFAULT_CONFIG = {
    'header_rows': 3,
    'spacing_rows': 2,
    'image_max_width': 700,
    'image_max_height': 500,
    'output_filename': 'screenshots.xlsx',
    'sheet_name_max_length': 31,
}

def setup_logging(level: str = 'INFO') -> logging.Logger:
    """Setup logging"""
    logger = logging.getLogger('exceltool')
    logger.setLevel(getattr(logging, level.upper()))
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logging()

def cleanup_old_temp_files(temp_base_dir: Path, max_age_hours: int = 24) -> int:
    """
    Clean up expired temporary files
    
    Args:
        temp_base_dir: Temporary file base directory
        max_age_hours: File maximum retention time (hours)，, default 24 hours
    
    Returns:
        Number of files/directories cleaned
    """
    if not temp_base_dir.exists():
        return 0
    
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    cleaned_count = 0
    
    try:
        for item in temp_base_dir.iterdir():
            try:
                # Skip cleanup record file
                if item.name == ".last_cleanup_date":
                    continue
                
                # Get file/directory modification time
                mtime = item.stat().st_mtime
                age = current_time - mtime
                
                # If file exceeds maximum retention time, delete it
                if age > max_age_seconds:
                    if item.is_dir():
                        shutil.rmtree(item)
                        logger.info(f"Clean up expired directory: {item}")
                    else:
                        item.unlink()
                        logger.info(f"Clean up expired file: {item}")
                    cleaned_count += 1
            except Exception as e:
                logger.warning(f"Failed to clean up file {item}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Failed to clean up temporary file directory: {e}")
    
    return cleaned_count

def check_and_cleanup(temp_base_dir: Path, cleanup_hour: int = 23, cleanup_minute: int = 59, max_age_hours: int = 24) -> bool:
    """
    Check time and execute cleanup
    
    Args:
        temp_base_dir: Temporary file base directory
        cleanup_hour: Cleanup time (hours)，, default 23
        cleanup_minute: Cleanup time (minutes), default 59
        max_age_hours: File maximum retention time (hours)，, default 24 hours
    
    Returns:
        Whether cleanup was executed
    """
    cleanup_record_file = temp_base_dir / ".last_cleanup_date"
    
    current_time = time.time()
    current_datetime = time.localtime(current_time)
    current_hour = current_datetime.tm_hour
    current_minute = current_datetime.tm_min
    current_date_str = time.strftime("%Y-%m-%d", current_datetime)
    
    # Check if cleanup time has arrived (5-minute window before and after cleanup time to ensure execution)
    time_window = 5  # 5minute window
    
    # Calculate start and end minutes of time window
    if cleanup_minute >= time_window:
        minute_start = cleanup_minute - time_window
        minute_end = cleanup_minute
        check_hour = cleanup_hour
    else:
        # If minutes are less than window, check last few minutes of previous hour
        minute_start = 60 - (time_window - cleanup_minute)
        minute_end = cleanup_minute
        check_hour = cleanup_hour
    
    # Check if within cleanup time window
    in_time_window = False
    
    # Case 1: Cleanup time in current hour (e.g., 23:59, window is 23:54-23:59)
    if cleanup_minute >= time_window:
        if current_hour == cleanup_hour and minute_start <= current_minute <= minute_end:
            in_time_window = True
    # Case 2: Cleanup time crosses hour boundary (e.g., 00:03, window is 23:58-00:03)
    else:
        if current_hour == cleanup_hour and current_minute <= minute_end:
            in_time_window = True
        elif current_hour == (cleanup_hour - 1) % 24 and current_minute >= minute_start:
            in_time_window = True
    
    if in_time_window:
        # Read last cleanup date
        last_cleanup_date = None
        if cleanup_record_file.exists():
            try:
                last_cleanup_date = cleanup_record_file.read_text().strip()
            except:
                pass
        
        # If not cleaned today, execute cleanup
        if last_cleanup_date != current_date_str:
            cleaned_count = cleanup_old_temp_files(temp_base_dir, max_age_hours=max_age_hours)
            if cleaned_count > 0:
                logger.info(f"Scheduled cleanup ({current_date_str} {cleanup_hour:02d}:{cleanup_minute:02d}): cleaned {cleaned_count} expired temporary files/directories")
            
            # Record this cleanup date
            try:
                cleanup_record_file.write_text(current_date_str)
            except:
                pass
            
            return True
    
    return False

def extract_zip_to_temp_dir(uploaded_zip, temp_base_dir: Path) -> Path:
    """Extract ZIP file to temporary directory, return extracted directory path"""
    # Create unique temporary directory
    import uuid
    extract_dir = temp_base_dir / f"extracted_{uuid.uuid4().hex[:8]}"
    extract_dir.mkdir(parents=True, exist_ok=True)
    
    # Save ZIP file
    zip_path = extract_dir / uploaded_zip.name
    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.getbuffer())
    
    # Extract ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # Delete ZIP file itself
    zip_path.unlink()
    
    return extract_dir

def save_uploaded_files_to_temp_dir(uploaded_files: List, temp_base_dir: Path) -> Path:
    """Save uploaded image files to temporary directory, return temporary directory path"""
    # Create unique temporary directory
    import uuid
    temp_dir = temp_base_dir / f"images_{uuid.uuid4().hex[:8]}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Save all uploaded files
    for uploaded_file in uploaded_files:
        file_path = temp_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    return temp_dir

def get_image_files(directory: Path) -> List[Path]:
    """Get all image files in directory"""
    image_files = []
    if not directory.exists():
        return image_files
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_IMAGE_FORMATS:
            image_files.append(file_path)
    image_files.sort(key=lambda x: x.name)
    return image_files

def get_subdirectories(directory: Path) -> List[Path]:
    """Get all subdirectories in directory"""
    subdirs = []
    if not directory.exists():
        return subdirs
    for item in directory.iterdir():
        if item.is_dir():
            subdirs.append(item)
    # Sort by directory name
    subdirs.sort(key=lambda x: x.name)
    return subdirs

def find_image_folders(root_dir: Path, ignore_dirs: set = None) -> List[Path]:
    """
    Recursively find all folders containing images (only return leaf folders containing images)
    
    Args:
        root_dir: Root directory path
        ignore_dirs: Set of folder names to ignore (such as _MACOSX, __MACOSX, etc.)
    
    Returns:
        List of folders containing images (only return folders directly containing images, not parent folders)
    """
    if ignore_dirs is None:
        ignore_dirs = {'_macosx', '__macosx', '.ds_store', '.git', '.svn', 'thumbs.db'}
    
    image_folders = []
    
    def _scan_directory(directory: Path):
        """Recursively scan directory to find all folders directly containing images"""
        # Skip system folders
        if directory.name.lower() in ignore_dirs:
            return
        
        # Check if current directory contains images
        image_files = get_image_files(directory)
        
        # Check subdirectories
        subdirs = get_subdirectories(directory)
        has_image_subdirs = False
        
        # First recursively check all subdirectories
        for subdir in subdirs:
            if subdir.name.lower() not in ignore_dirs:
                _scan_directory(subdir)
                # Check if subdirectory contains images
                if get_image_files(subdir):
                    has_image_subdirs = True
        
        # If current directory contains images, and no subdirectories contain images, add current directory
        # This avoids duplication: if both parent and child folders have images, only add child folder
        if image_files and not has_image_subdirs:
            image_folders.append(directory)
    
    _scan_directory(root_dir)
    
    # Sort by path
    image_folders.sort(key=lambda x: str(x))
    return image_folders

def sanitize_sheet_name(name: str) -> str:
    """Sanitize sheet name to ensure it meets Excel requirements"""
    invalid_chars = ['\\', '/', '*', '?', ':', '[', ']']
    for char in invalid_chars:
        name = name.replace(char, '_')
    max_length = DEFAULT_CONFIG['sheet_name_max_length']
    if len(name) > max_length:
        name = name[:max_length]
    if not name.strip():
        name = 'Sheet'
    return name.strip()

class ImageProcessor:
    """Image processor"""
    def __init__(self, max_width: int = None, max_height: int = None, 
                 fixed_width: int = None, fixed_height: int = None):
        self.max_width = max_width or DEFAULT_CONFIG['image_max_width']
        self.max_height = max_height or DEFAULT_CONFIG['image_max_height']
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height
    
    def resize_image(self, image_path: Path) -> Tuple[ExcelImage, Tuple[int, int]]:
        """Adjust image size and convert to ExcelImage object"""
        import io
        try:
            with Image.open(image_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                width, height = img.size
                
                if self.fixed_width and self.fixed_height:
                    new_width = self.fixed_width
                    new_height = self.fixed_height
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                elif self.fixed_width:
                    scale = self.fixed_width / width
                    new_width = self.fixed_width
                    new_height = int(height * scale)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                elif self.fixed_height:
                    scale = self.fixed_height / height
                    new_width = int(width * scale)
                    new_height = self.fixed_height
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    scale_w = self.max_width / width if width > self.max_width else 1
                    scale_h = self.max_height / height if height > self.max_height else 1
                    scale = min(scale_w, scale_h, 1)
                    
                    if scale < 1:
                        new_width = int(width * scale)
                        new_height = int(height * scale)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    else:
                        new_width, new_height = width, height
                
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                excel_img = ExcelImage(img_buffer)
                excel_img.width = new_width
                excel_img.height = new_height
                
                return excel_img, (new_width, new_height)
        except Exception as e:
            logger.error(f"Processing image {image_path} error occurred: {e}")
            raise

class ExcelProcessor:
    """Excel processor"""
    def __init__(self, header_rows: int = None, spacing_rows: int = None, show_titles: bool = True, respect_header_rows: bool = True):
        self.header_rows = header_rows or DEFAULT_CONFIG['header_rows']
        self.spacing_rows = spacing_rows or DEFAULT_CONFIG['spacing_rows']
        self.show_titles = show_titles
        self.respect_header_rows = respect_header_rows
        self.image_processor = ImageProcessor()
        self.workbook = None
        self.current_row = {}
    
    def create_workbook(self) -> Workbook:
        """Create new workbook"""
        self.workbook = Workbook()
        if 'Sheet' in self.workbook.sheetnames:
            self.workbook.remove(self.workbook['Sheet'])
        return self.workbook
    
    def load_workbook(self, file_path: Path) -> Workbook:
        """Load existing workbook (supports .xlsx and .xls formats)"""
        try:
            file_ext = file_path.suffix.lower()
            
            # If .xls format, need to convert to .xlsx first
            if file_ext == '.xls':
                if not XLS_SUPPORT:
                    raise ImportError("Need to install pandas and xlrd libraries to support .xls format files")
                
                # Use pandas to read .xls file
                xls_file = pd.ExcelFile(file_path)
                
                # Create temporary .xlsx file
                temp_xlsx = file_path.parent / f"{file_path.stem}_temp.xlsx"
                with pd.ExcelWriter(temp_xlsx, engine='openpyxl') as writer:
                    for sheet_name in xls_file.sheet_names:
                        df = pd.read_excel(xls_file, sheet_name=sheet_name)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Use openpyxl to load converted file
                self.workbook = load_workbook(temp_xlsx)
                
                # Delete temporary file
                try:
                    temp_xlsx.unlink()
                except:
                    pass
            else:
                # Directly use openpyxl to load .xlsx file
                self.workbook = load_workbook(file_path)
            
            # Initialize current_row
            for sheet_name in self.workbook.sheetnames:
                if sheet_name not in self.current_row:
                    sheet = self.workbook[sheet_name]
                    max_row = sheet.max_row
                    if self.respect_header_rows:
                        self.current_row[sheet_name] = self.header_rows + 1
                    else:
                        if max_row > 0:
                            for row in range(max_row, max(1, max_row - 5), -1):
                                if any(cell.value for cell in sheet[row]):
                                    self.current_row[sheet_name] = row + 1
                                    break
                            else:
                                self.current_row[sheet_name] = self.header_rows + 1
                        else:
                            self.current_row[sheet_name] = self.header_rows + 1
            return self.workbook
        except Exception as e:
            logger.error(f"Failed to load workbook {file_path}: {e}")
            raise
    
    def get_or_create_sheet(self, sheet_name: str) -> str:
        """Get or create worksheet"""
        if not self.workbook:
            self.create_workbook()
        
        clean_name = sanitize_sheet_name(sheet_name)
        existing_sheet = self.find_sheet_by_name(clean_name)
        
        if existing_sheet:
            return existing_sheet
        else:
            sheet = self.workbook.create_sheet(title=clean_name)
            self.current_row[clean_name] = self.header_rows + 1
            # Set column width: Column A for titles, need wide enough to display filename (60 characters wide)
            sheet.column_dimensions['A'].width = 60
            sheet.column_dimensions['B'].width = 100
            return clean_name
    
    def find_sheet_by_name(self, target_name: str) -> Optional[str]:
        """Find worksheet by name (case-insensitive)"""
        if not self.workbook:
            return None
        target_lower = target_name.lower()
        for sheet_name in self.workbook.sheetnames:
            if sheet_name.lower() == target_lower:
                return sheet_name
        return None
    
    def add_image_to_sheet(self, sheet_name: str, image_path: Path, image_title: str = None) -> None:
        """Add image to specified worksheet"""
        if not self.workbook:
            logger.error("Workbook does not exist")
            return
        
        actual_sheet_name = self.find_sheet_by_name(sheet_name)
        if not actual_sheet_name:
            logger.error(f"Worksheet {sheet_name}  does not exist")
            return
        
        sheet = self.workbook[actual_sheet_name]
        
        if actual_sheet_name not in self.current_row:
            max_row = sheet.max_row
            if max_row > 0:
                for row in range(max_row, max(1, max_row - 5), -1):
                    if any(cell.value for cell in sheet[row]):
                        self.current_row[actual_sheet_name] = row + 1
                        break
                else:
                    self.current_row[actual_sheet_name] = self.header_rows + 1
            else:
                self.current_row[actual_sheet_name] = self.header_rows + 1
        
        current_row = self.current_row.get(actual_sheet_name, self.header_rows + 1)
        
        try:
            excel_img, (width, height) = self.image_processor.resize_image(image_path)
            
            if self.show_titles and image_title:
                title_cell = sheet.cell(row=current_row, column=1)
                title_cell.value = image_title
                title_cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
                # Set title row height to ensure filename is not obscured
                sheet.row_dimensions[current_row].height = 40
                # Ensure column width is sufficient to display filename
                if sheet.column_dimensions['A'].width < 60:
                    sheet.column_dimensions['A'].width = 60
                current_row += 1
            
            # Image inserted below title row
            excel_img.anchor = f'A{current_row}'
            sheet.add_image(excel_img)
            
            # Set image row height to ensure image fully displays and doesn't obscure next row content
            row_height_points = height * 0.75  #  pixels to points
            
            # Dynamically adjust extra space based on image height
            if height < 300:
                extra_space = 30
            elif height < 600:
                extra_space = 40
            else:
                extra_space = 50
            
            row_height = row_height_points + extra_space
            
            # Ensure minimum row height to avoid row height too small
            if row_height < 120:
                row_height = 120
            
            sheet.row_dimensions[current_row].height = row_height
            
            # When updating to next row, ensure skip enough rows
            current_row += 1 + self.spacing_rows
            self.current_row[sheet_name] = current_row
            
        except Exception as e:
            logger.error(f"Failed to add image {image_path} to {sheet_name}: {e}")
    
    def process_directory(self, directory: Path, sheet_name: str = None) -> None:
        """Process all images in directory"""
        if not sheet_name:
            sheet_name = directory.name
        
        actual_sheet_name = self.get_or_create_sheet(sheet_name)
        image_files = get_image_files(directory)
        
        if not image_files:
            logger.warning(f"Directory {directory}  has no image files found")
            return
        
        for i, image_path in enumerate(image_files, 1):
            image_title = f"{i}. {image_path.stem}"
            self.add_image_to_sheet(actual_sheet_name, image_path, image_title)
    
    def save_workbook(self, output_path: Path) -> None:
        """Save workbook"""
        if not self.workbook:
            logger.error("No workbook to save")
            return
        try:
            self.workbook.save(output_path)
            logger.info(f"Workbook saved to: {output_path}")
        except Exception as e:
            logger.error(f"Failed to save workbook {output_path}: {e}")
            raise


def render_excel_tool():
    """Render Excel tool interface"""
    st.markdown("## 📊 Excel Tool - Screenshot to Excel")
    
    st.info("Batch insert screenshot files from directory into Excel files, supports creating new files or appending to existing files")
    
    # Offline version download
    with st.expander("💻 Offline Version Download (Click to expand)", expanded=False):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            **Offline version tool available, works without internet connection!**
            
            - ✅ Fully offline operation, protects data privacy
            - ✅ Supports batch processing of large numbers of images
            - ✅ Same functionality as online version
            """)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Vertical centering
            tool_path = Path(__file__).parent.parent.parent / "ExcelScreenshotTool"
            if tool_path.exists():
                with open(tool_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download Offline Version",
                        data=f.read(),
                        file_name="ExcelScreenshotTool",
                        mime="application/octet-stream",
                        use_container_width=True,
                        help="Download Excel Screenshot Tool offline version (macOS ARM64)"
                    )
            else:
                st.warning("⚠️ Offline version file not found")
    

    
    # Usage instructions
    with st.expander("📖 Detailed Usage Instructions (Click to expand)", expanded=False):
        st.markdown("""
        ### 📁 File Upload Settings
        
        #### Upload Method
        - **Type**: Radio button
        - **Options**: 
          - **ZIP File (Recommended - Preserve folder structure)**: Upload ZIP archive, preserves folder structure, each folder corresponds to one Sheet (recommended method)
          - **Multiple Image Files**: Upload multiple image files, all images placed in the same Sheet
        - **Notes**: 
          - ⚠️ **Browser limitations**: Browsers don't support direct folder selection, only individual file selection
          - 💡 **Recommended: Use ZIP file method**: Can upload entire folder at once, more convenient and faster
          - ZIP file method supports folder structure, each folder creates a corresponding Sheet
        - **ZIP File Notes**: 
          - ZIP file will be automatically extracted after upload
          - If ZIP contains multiple subfolders, each folder creates a corresponding Sheet
          - Folder name becomes the Sheet name
          - If ZIP has no subfolders, all images go into a Sheet named "Screenshots"
        - **Multiple Image Files Notes**:
          - ⚠️ Browser limitations prevent direct folder selection, need to select image files individually
          - Can select multiple image files at once (using Ctrl/Cmd+click for multi-select)
          - All images placed in the same Sheet named "Screenshots"
          - Images sorted by filename
          - 💡 If many files (>10), strongly recommend using ZIP file method
        
        #### File Mode
        - **Type**: Checkbox
        - **Option**: "Use existing Excel file"
        - **Description**: Toggle file mode
          - **Unchecked** (default): Create new Excel file, can download after processing
          - **Checked**: Append to existing Excel file, can download after processing
        - **Effect**: Shows/hides corresponding file selection options when toggled
        
        #### Existing Excel File
        - **Type**: File uploader
        - **Visibility**: Only shown in "Use existing Excel file" mode
        - **Description**: Upload Excel file to append screenshots
        - **Operation**: Use file uploader to upload Excel file (supports .xlsx and .xls formats)
        - **Validation**: File must be valid and in .xlsx or .xls format
        - **Note**: If uploading .xls format file, need to install pandas and xlrd libraries (will be installed automatically)
        
        #### File Download
        - **Description**: Excel file will be automatically generated and download button provided after processing
        - **New mode**: Filename format `screenshots_{timestamp}.xlsx`
        - **Append mode**: Filename format `updated_{original_filename}_{timestamp}.xlsx`
        
        ### 🖼️ Image Settings
        
        #### Max Width
        - **Type**: Number input
        - **Unit**: Pixels
        - **Default**: `700`
        - **Description**: Maximum width limit for images
        - **Purpose**: Works with Max Height to limit maximum size while maintaining image aspect ratio
        - **Note**: Only effective when fixed dimensions are not set
        
        #### Max Height
        - **Type**: Number input
        - **Unit**: Pixels
        - **Default**: `500`
        - **Description**: Maximum height limit for images
        - **Purpose**: Works with Max Width to limit maximum size while maintaining image aspect ratio
        - **Note**: Only effective when fixed dimensions are not set
        
        #### Fixed Width
        - **Type**: Checkbox + Number input (optional)
        - **Unit**: Pixels
        - **Default**: Not used (input box appears when checkbox is checked)
        - **Description**: Force all images to fixed width
        - **Usage**:
          - Only set Fixed Width: Height scales proportionally
          - Set both Fixed Width and Fixed Height: Force to specified dimensions
        - **Note**: Mutually exclusive with Max Width, ignores maximum width when fixed width is set
        
        #### Fixed Height
        - **Type**: Checkbox + Number input (optional)
        - **Unit**: Pixels
        - **Default**: Not used (input box appears when checkbox is checked)
        - **Description**: Force all images to fixed height
        - **Usage**:
          - Only set Fixed Height: Width scales proportionally
          - Set both Fixed Width and Fixed Height: Force to specified dimensions
        - **Note**: Mutually exclusive with Max Height, ignores maximum height when fixed height is set
        
        #### Hide image titles
        - **Type**: Checkbox
        - **Default**: Unchecked (show titles)
        - **Description**: Control whether to show filename title before images
        - **Effect**:
          - **Unchecked**: Show "1. Image Name" format title before each image
          - **Checked**: Only insert images, no titles displayed
        
        ### 📐 Layout Settings
        
        #### Header Rows
        - **Type**: Number input
        - **Default**: `3`
        - **Description**: Reserved rows at top of Excel worksheet
        - **Purpose**: Images start inserting from row `header_rows + 1`
        - **Use case**: When need to add headers, descriptions, etc. at top of Excel
        
        #### Image Spacing
        - **Type**: Number input
        - **Unit**: Rows
        - **Default**: `2`
        - **Description**: Number of empty rows between images
        - **Purpose**: Controls spacing between images, improves readability
        - **Range**: Recommended 0-10
        
        ### 🔘 Action Buttons
        
        #### Start Processing
        - **Function**: Start processing screenshots and generate Excel file
        - **Validation**: Validates all inputs before clicking
        - **Status**: Shows progress bar during processing
        - **Progress**: Bottom status bar shows processing progress
        - **Completion**: Shows success message and download button after processing
        
        #### Clear
        - **Function**: Clear all inputs, restore defaults
        - **Operation**: Clears all fields and selections
        
        #### Exit
        - **Function**: Close program
        
        ### ⚠️ Notes
        
        - Need to install `openpyxl` and `Pillow` libraries: `pip install openpyxl Pillow`
        - To support .xls format, also need to install: `pip install pandas xlrd`
        - Image files will be sorted by filename before insertion
        - Processing large files may take some time, please be patient
        - Output directory will be created automatically if it doesn't exist
        - Supports multi-folder processing: If input path has multiple subfolders, each folder creates a corresponding Sheet
        """)
    
    st.markdown("---")
    
    # Initialize session state
    if 'last_input_path' not in st.session_state:
        st.session_state.last_input_path = ""
    if 'last_excel_path' not in st.session_state:
        st.session_state.last_excel_path = ""
    if 'uploaded_files_dir' not in st.session_state:
        st.session_state.uploaded_files_dir = None
    
    # File upload settings
    st.markdown("### 📁 File Upload Settings")
    
    # Upload method selection
    upload_mode = st.radio(
        "Upload Method",
        ["📦 ZIP File (Recommended - Preserve folder structure)", "🖼️ Multiple Image Files"],
        help="💡 Recommended: Use ZIP file method - can upload entire folder at once, preserves folder structure, each folder corresponds to one Sheet"
    )
    
    # Create temporary directory for storing uploaded files
    temp_base_dir = Path(os.path.join(os.path.expanduser("~"), ".streamlit_temp"))
    temp_base_dir.mkdir(parents=True, exist_ok=True)
    
    # Regularly clean up expired temporary files (default: daily at 23:59, keep files within 24 hours)
    check_and_cleanup(temp_base_dir, cleanup_hour=23, cleanup_minute=59, max_age_hours=24)
    
    uploaded_files_path = None
    
    if upload_mode == "📦 ZIP File (Recommended - Preserve folder structure)":
        uploaded_zip = st.file_uploader(
            "Upload ZIP File",
            type=["zip"],
            help="Upload ZIP archive containing image files, folder structure will be preserved (each folder corresponds to one Sheet)",
            key="upload_zip"
        )
        
        if uploaded_zip:
            try:
                # Extract ZIP file
                logger.info(f"Start extracting ZIP file: {uploaded_zip.name}")
                with st.spinner("Extracting ZIP file..."):
                    extracted_dir = extract_zip_to_temp_dir(uploaded_zip, temp_base_dir)
                    st.session_state.uploaded_files_dir = str(extracted_dir)
                    uploaded_files_path = extracted_dir
                    st.success(f"✅ ZIP file extracted: {uploaded_zip.name}")
                    logger.info(f"ZIP file extracted successfully: {uploaded_zip.name} -> {extracted_dir}")
                    
                    # Display folder structure preview
                    # Use intelligent find function to find all folders containing images
                    image_folders = find_image_folders(extracted_dir)
                    
                    if image_folders:
                        st.info(f"📁 Detected {len(image_folders)} folders containing images, will create corresponding Sheets")
                        logger.info(f"Detected {len(image_folders)} folders containing images")
                        with st.expander("View folder structure"):
                            for folder in image_folders:
                                image_count = len(get_image_files(folder))
                                # Display relative path for clarity
                                relative_path = folder.relative_to(extracted_dir)
                                st.write(f"- {relative_path}: {image_count} images")
                                logger.debug(f"Folder: {relative_path}, contains {image_count} images")
                    else:
                        # If no folders containing images found, check if root directory has images
                        image_count = len(get_image_files(extracted_dir))
                        if image_count > 0:
                            st.info(f"📁 Detected {image_count} images, will be placed in 'Screenshots' Sheet")
                            logger.info(f"Root directory contains {image_count} images")
                        else:
                            st.warning("⚠️ No image files found, please check ZIP file contents")
                            logger.warning("No image files found in ZIP file")
            except Exception as e:
                st.error(f"❌ Failed to extract ZIP file: {str(e)}")
                logger.error(f"Failed to extract ZIP file: {e}", exc_info=True)
                uploaded_files_path = None
    
    else:  # Multiple image files
        st.info("💡 **Tip**: Browsers don't support direct folder selection. If you need to upload multiple files, recommend using ZIP file method (option above) to upload entire folder at once.")
        
        uploaded_images = st.file_uploader(
            "Upload Image Files (Multiple)",
            type=["png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff"],
            accept_multiple_files=True,
            help="⚠️ Note: Browser limitations prevent direct folder selection. If uploading many files, recommend using ZIP file method. Current method requires selecting image files individually.",
            key="upload_images"
        )
        
        if uploaded_images:
            if len(uploaded_images) > 10:
                st.warning(f"⚠️ You selected {len(uploaded_images)} files. If you have many files, recommend using ZIP file method for easier upload.")
            
            try:
                # Save uploaded image files
                logger.info(f"Start saving {len(uploaded_images)} image files")
                with st.spinner("Saving image files..."):
                    images_dir = save_uploaded_files_to_temp_dir(uploaded_images, temp_base_dir)
                    st.session_state.uploaded_files_dir = str(images_dir)
                    uploaded_files_path = images_dir
                    st.success(f"✅ Uploaded {len(uploaded_images)} images")
                    logger.info(f"Image files saved successfully: {len(uploaded_images)} images -> {images_dir}")
            except Exception as e:
                st.error(f"❌ Failed to save image files: {str(e)}")
                logger.error(f"Failed to save image files: {e}", exc_info=True)
                uploaded_files_path = None
    
    # If using uploaded files, use uploaded file path
    if st.session_state.uploaded_files_dir:
        uploaded_files_path = Path(st.session_state.uploaded_files_dir)
    
    # File mode
    use_existing_file = st.checkbox(
        "File Mode: Use existing Excel file",
        value=False,
        help="Unchecked: Create new Excel file (can download after processing); Checked: Append to existing Excel file"
    )
    
    # Existing file settings (only shown in append mode)
    if use_existing_file:
        uploaded_file = st.file_uploader(
            "Existing Excel File",
            type=["xlsx", "xls"],
            help="Upload Excel file to append screenshots (supports .xlsx and .xls formats)",
            key="upload_excel"
        )
        
        if uploaded_file:
            temp_dir = os.path.join(os.path.expanduser("~"), ".streamlit_temp")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            logger.info(f"Saving uploaded Excel file: {uploaded_file.name} -> {temp_path}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.excel_existing_file = temp_path
            st.info(f"📁 File uploaded: {uploaded_file.name}")
            logger.info(f"Excel file uploaded successfully: {uploaded_file.name}")
            
            # If .xls format, prompt to install dependencies
            if uploaded_file.name.lower().endswith('.xls') and not XLS_SUPPORT:
                st.warning("⚠️ Detected .xls format file, need to install pandas and xlrd libraries. Run: pip install pandas xlrd")
                logger.warning("Detected .xls format file but pandas/xlrd libraries not installed")
    else:
        st.info("ℹ️ Will create new Excel file, can download directly after processing")
    
    st.markdown("---")
    
    # Image settings
    st.markdown("### 🖼️ Image Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_width = st.number_input(
            "Max Width (pixels)",
            min_value=1,
            value=700,
            help="Maximum width limit for images, works with Max Height to limit maximum size while maintaining image aspect ratio"
        )
        
        use_fixed_width = st.checkbox("Use Fixed Width", value=False, key="use_fixed_width")
        fixed_width = None
        if use_fixed_width:
            fixed_width = st.number_input(
                "Fixed Width (pixels)",
                min_value=1,
                value=800,
                help="Force all images to fixed width. Only set Fixed Width: height scales proportionally; Set both Fixed Width and Fixed Height: force to specified dimensions.",
                key="fixed_width_input"
            )
    
    with col2:
        max_height = st.number_input(
            "Max Height (pixels)",
            min_value=1,
            value=500,
            help="Maximum height limit for images, works with Max Width to limit maximum size while maintaining image aspect ratio"
        )
        
        use_fixed_height = st.checkbox("Use Fixed Height", value=False, key="use_fixed_height")
        fixed_height = None
        if use_fixed_height:
            fixed_height = st.number_input(
                "Fixed Height (pixels)",
                min_value=1,
                value=600,
                help="Force all images to fixed height. Only set Fixed Height: width scales proportionally; Set both Fixed Width and Fixed Height: force to specified dimensions.",
                key="fixed_height_input"
            )
    
    hide_image_titles = st.checkbox(
        "Hide image titles",
        value=False,
        help="Check to insert images only, without displaying filename titles"
    )
    
    st.markdown("---")
    
    # Layout settings
    st.markdown("### 📐 Layout Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        header_rows = st.number_input(
            "Header Rows",
            min_value=0,
            value=3,
            help="Reserved rows at top of Excel worksheet, images will start inserting from row header_rows+1"
        )
    
    with col2:
        image_spacing = st.number_input(
            "Image Spacing (rows)",
            min_value=0,
            value=2,
            help="Number of empty rows between images, controls spacing between images"
        )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        process_button = st.button("🚀 Start Processing", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    with col3:
        exit_button = st.button("🚪 Exit", use_container_width=True)
    
    # Clear button logic
    if clear_button:
        logger.info("User clicked clear button, starting to clean up temporary files and state")
        
        # Clean up uploaded file directory
        if st.session_state.get('uploaded_files_dir'):
            try:
                temp_path = Path(st.session_state.uploaded_files_dir)
                if temp_path.exists():
                    shutil.rmtree(temp_path)
                    logger.info(f"Deleted uploaded file directory: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to delete uploaded file directory: {e}")
        
        # Clean up uploaded Excel file
        if st.session_state.get('excel_existing_file'):
            try:
                excel_file = Path(st.session_state.excel_existing_file)
                if excel_file.exists():
                    excel_file.unlink()
                    logger.info(f"Deleted uploaded Excel file: {excel_file}")
            except Exception as e:
                logger.warning(f"Failed to delete Excel file: {e}")
        
        # Clean up generated output file
        if st.session_state.get('last_output_file'):
            try:
                output_file = Path(st.session_state.last_output_file)
                if output_file.exists():
                    output_file.unlink()
                    logger.info(f"Deleted generated output file: {output_file}")
            except Exception as e:
                logger.warning(f"Failed to delete output file: {e}")
        
        # Clear session state
        st.session_state.excel_input_path = ""
        st.session_state.excel_existing_file = ""
        st.session_state.uploaded_files_dir = None
        st.session_state.last_output_file = None
        
        logger.info("Clear operation completed")
        st.rerun()
    
    # Exit button logic
    if exit_button:
        logger.info("User clicked exit button, starting to clean up temporary files and state")
        
        # Clean up uploaded file directory
        if st.session_state.get('uploaded_files_dir'):
            try:
                temp_path = Path(st.session_state.uploaded_files_dir)
                if temp_path.exists():
                    shutil.rmtree(temp_path)
                    logger.info(f"Deleted uploaded file directory: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to delete uploaded file directory: {e}")
        
        # Clean up uploaded Excel file
        if st.session_state.get('excel_existing_file'):
            try:
                excel_file = Path(st.session_state.excel_existing_file)
                if excel_file.exists():
                    excel_file.unlink()
                    logger.info(f"Deleted uploaded Excel file: {excel_file}")
            except Exception as e:
                logger.warning(f"Failed to delete Excel file: {e}")
        
        # Clean up generated output file
        if st.session_state.get('last_output_file'):
            try:
                output_file = Path(st.session_state.last_output_file)
                if output_file.exists():
                    output_file.unlink()
                    logger.info(f"Deleted generated output file: {output_file}")
            except Exception as e:
                logger.warning(f"Failed to delete output file: {e}")
        
        logger.info("Exit operation completed")
        st.stop()
    
    # Process button logic
    if process_button:
        errors = []
        
        # Validate input path
        if not uploaded_files_path or not uploaded_files_path.exists():
            errors.append("❌ Please upload files first (ZIP file or image files)")
        
        if use_existing_file:
            existing_file = st.session_state.get('excel_existing_file', "")
            if not existing_file or not os.path.isfile(existing_file):
                errors.append("❌ Please upload an existing Excel file")
            elif not existing_file.lower().endswith(('.xlsx', '.xls')):
                errors.append("❌ Excel file must be in .xlsx or .xls format")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                logger.info("Start processing Excel file")
                # Determine path to process
                input_path_obj = Path(uploaded_files_path)
                
                logger.info(f"Input path: {input_path_obj}")
                
                # Create Excel processor
                processor = ExcelProcessor(
                    header_rows=header_rows,
                    spacing_rows=image_spacing,
                    show_titles=not hide_image_titles,
                    respect_header_rows=True
                )
                
                # Set image processor parameters
                processor.image_processor.max_width = max_width
                processor.image_processor.max_height = max_height
                processor.image_processor.fixed_width = fixed_width
                processor.image_processor.fixed_height = fixed_height
                
                # Process Excel file
                if use_existing_file:
                    existing_file = st.session_state.get('excel_existing_file', "")
                    processor.load_workbook(Path(existing_file))
                else:
                    processor.create_workbook()
                
                # Check for folders containing images (intelligent search)
                image_folders = find_image_folders(input_path_obj)
                
                if image_folders:
                    # Has folders containing images: create a sheet for each folder
                    total_images = 0
                    processed_images = 0
                    
                    # First count total images
                    for folder in image_folders:
                        image_files = get_image_files(folder)
                        total_images += len(image_files)
                    
                    if total_images == 0:
                        st.warning("⚠️ No image files found in folders (supported: png, jpg, jpeg, gif, bmp, webp)")
                    else:
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Process each folder containing images
                        for folder in image_folders:
                            # Use folder name as sheet name
                            sheet_name = folder.name
                            image_files = get_image_files(folder)
                            
                            if image_files:
                                status_text.text(f"Processing folder: {sheet_name} ({len(image_files)}  images)")
                                logger.info(f"Start processing folder: {sheet_name}, contains {len(image_files)}  images")
                                
                                # Get or create worksheet (use folder name as sheet name)
                                actual_sheet_name = processor.get_or_create_sheet(sheet_name)
                                logger.info(f"Processing Sheet: {actual_sheet_name}, contains {len(image_files)}  images")
                                
                                # Process images one by one
                                for idx, image_path in enumerate(image_files, 1):
                                    status_text.text(f"Processing: {sheet_name}/{image_path.name} ({processed_images + idx}/{total_images})")
                                    image_title = f"{idx}. {image_path.stem}"
                                    logger.debug(f"Adding image to Sheet: {actual_sheet_name}, image: {image_path.name}")
                                    processor.add_image_to_sheet(actual_sheet_name, image_path, image_title)
                                    progress_bar.progress((processed_images + idx) / total_images)
                                
                                logger.info(f"Sheet {actual_sheet_name} processing completed, processed {len(image_files)}  images")
                                processed_images += len(image_files)
                        
                        # Save file to temporary directory
                        temp_dir = os.path.join(os.path.expanduser("~"), ".streamlit_temp")
                        os.makedirs(temp_dir, exist_ok=True)
                        
                        if use_existing_file:
                            # Append mode: save to new temporary file (don't overwrite original)
                            output_filename = f"updated_{Path(existing_file).stem}_{int(time.time())}.xlsx"
                        else:
                            # New mode
                            output_filename = f"screenshots_{int(time.time())}.xlsx"
                        
                        output_path = Path(temp_dir) / output_filename
                        
                        status_text.text("Saving Excel file...")
                        logger.info(f"Saving Excel file to: {output_path}")
                        processor.save_workbook(output_path)
                        logger.info(f"Excel file saved successfully: {output_path}")
                        
                        # Save output file path for download
                        st.session_state.last_output_file = str(output_path)
                        
                        # Clean up temporary files
                        if uploaded_files_path and uploaded_files_path.exists():
                            try:
                                shutil.rmtree(uploaded_files_path)
                                logger.info(f"Processing completed, deleted uploaded file directory: {uploaded_files_path}")
                            except Exception as e:
                                logger.warning(f"Failed to delete uploaded file directory: {e}")
                        
                        # Completion message
                        progress_bar.progress(1.0)
                        status_text.empty()
                        st.success(f"✅ Processing completed! Processed {len(image_folders)} Sheets (corresponding to {len(image_folders)} folders),{total_images}  images。")
                        
                        # Provide download link
                        logger.info(f"Preparing to download Excel file: {output_filename} (path: {output_path})")
                        with open(output_path, 'rb') as f:
                            file_data = f.read()
                            download_clicked = st.download_button(
                                label="📥 Download Excel File",
                                data=file_data,
                                file_name=output_filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_{int(time.time())}"
                            )
                            
                            # If download button clicked, delay file deletion (give user time to download)
                            if download_clicked:
                                logger.info(f"User clicked download button, file: {output_filename}")
                                # Delete file after delay (60 seconds)
                                import threading
                                def delayed_delete(file_path, delay=60):
                                    """Delete file after delay (60 seconds)"""
                                    time.sleep(delay)
                                    try:
                                        if Path(file_path).exists():
                                            Path(file_path).unlink()
                                            logger.info(f"Delayed deletion of output file: {file_path}")
                                    except Exception as e:
                                        logger.warning(f"Failed to delete file {file_path}: {e}")
                                
                                thread = threading.Thread(target=delayed_delete, args=(output_path,))
                                thread.daemon = True
                                thread.start()
                else:
                    # No subfolders: process images in current directory
                    image_files = get_image_files(input_path_obj)
                    
                    if not image_files:
                        st.warning("⚠️ No image files found in specified directory (supported: png, jpg, jpeg, gif, bmp, webp)")
                    else:
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Get or create worksheet
                        actual_sheet_name = processor.get_or_create_sheet("Screenshots")
                        logger.info(f"Processing Sheet: {actual_sheet_name}, contains {len(image_files)} images")
                        
                        # Process images one by one and show progress
                        for idx, image_path in enumerate(image_files, 1):
                            status_text.text(f"Processing: {image_path.name} ({idx}/{len(image_files)})")
                            image_title = f"{idx}. {image_path.stem}"
                            logger.debug(f"Adding image to Sheet: {actual_sheet_name}, image: {image_path.name}")
                            processor.add_image_to_sheet(actual_sheet_name, image_path, image_title)
                            progress_bar.progress(idx / len(image_files))
                        
                        logger.info(f"Sheet {actual_sheet_name} processing completed, processed {len(image_files)}  images")
                        
                        # Save file to temporary directory
                        temp_dir = os.path.join(os.path.expanduser("~"), ".streamlit_temp")
                        os.makedirs(temp_dir, exist_ok=True)
                        
                        if use_existing_file:
                            # Append mode: save to new temporary file (don't overwrite original)
                            output_filename = f"updated_{Path(existing_file).stem}_{int(time.time())}.xlsx"
                        else:
                            # New mode
                            output_filename = f"screenshots_{int(time.time())}.xlsx"
                        
                        output_path = Path(temp_dir) / output_filename
                        
                        status_text.text("Saving Excel file...")
                        logger.info(f"Saving Excel file to: {output_path}")
                        processor.save_workbook(output_path)
                        logger.info(f"Excel file saved successfully: {output_path}")
                        
                        # Save output file path for download
                        st.session_state.last_output_file = str(output_path)
                        
                        # Clean up temporary files
                        if uploaded_files_path and uploaded_files_path.exists():
                            try:
                                shutil.rmtree(uploaded_files_path)
                                logger.info(f"Processing completed, deleted uploaded file directory: {uploaded_files_path}")
                            except Exception as e:
                                logger.warning(f"Failed to delete uploaded file directory: {e}")
                        
                        # Completion message
                        progress_bar.progress(1.0)
                        status_text.empty()
                        st.success(f"✅ Processing completed! Processed {len(image_files)}  images。")
                        
                        # Provide download link
                        logger.info(f"Preparing to download Excel file: {output_filename} (path: {output_path})")
                        with open(output_path, 'rb') as f:
                            file_data = f.read()
                            download_clicked = st.download_button(
                                label="📥 Download Excel File",
                                data=file_data,
                                file_name=output_filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_{int(time.time())}"
                            )
                            
                            # If download button clicked, mark file for deletion
                            # Note: Due to Streamlit limitations, cannot directly detect download completion, so will delete on next clear or exit
                            if download_clicked:
                                logger.info(f"User clicked download button, file: {output_filename}")
                                # Delay file deletion (give user time to download)
                                import threading
                                def delayed_delete(file_path, delay=60):
                                    """Delete file after delay (60 seconds)"""
                                    time.sleep(delay)
                                    try:
                                        if Path(file_path).exists():
                                            Path(file_path).unlink()
                                            logger.info(f"Delayed deletion of output file: {file_path}")
                                    except Exception as e:
                                        logger.warning(f"Failed to delete file {file_path}: {e}")
                                
                                thread = threading.Thread(target=delayed_delete, args=(output_path,))
                                thread.daemon = True
                                thread.start()
                    
            except Exception as e:
                st.error(f"❌ Error occurred during processing: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

