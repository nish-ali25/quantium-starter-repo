import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from app import app

def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    
    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")
    assert header.text == "Soul Foods: Pink Morsel Sales Visualiser"

def test_visualization_is_present(dash_duo):
    dash_duo.start_server(app)
    
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    chart = dash_duo.find_element("#sales-line-chart")
    assert chart is not None

def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)
    
    dash_duo.wait_for_element("#region-selector", timeout=10)
    region_picker = dash_duo.find_element("#region-selector")
    assert region_picker is not None