import requests
import json

# Your server URL
MCP_SERVER = "https://167aliraza-weather-mcp-server.hf.space"

def test_mcp_server():
    """Test if MCP server is accessible"""
    
    # Test 1: Check if server is running
    print("🔍 Testing server health...")
    try:
        response = requests.get(f"{MCP_SERVER}/")
        print(f"✅ Server is running: {response.json()}")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return
    
    # Test 2: Check MCP endpoint
    print("\n🔍 Testing MCP endpoint...")
    try:
        response = requests.get(f"{MCP_SERVER}/mcp")
        print(f"✅ MCP endpoint accessible")
    except Exception as e:
        print(f"❌ MCP endpoint error: {e}")
    
    # Test 3: Test weather tool directly
    print("\n🔍 Testing weather tool...")
    try:
        # Test current weather
        response = requests.post(
            f"{MCP_SERVER}/mcp/tools/get_weather_data",
            json={
                "city_name": "London",
                "query_type": "current"
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Weather tool works!")
            print(f"\n📊 Sample data:")
            print(json.dumps(data, indent=2)[:500] + "...")
        else:
            print(f"❌ Tool error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Weather tool error: {e}")

# if __name__ == "__main__":
test_mcp_server()