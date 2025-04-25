import streamlit as st
import requests

# 抓書店資料
def getAllBookstore():
    url = "https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

# 取得所有縣市選項
def getCountyOptions(bookstoreList):
    counties = set()
    for store in bookstoreList:
        if store.get("cityName"):
            counties.add(store["cityName"].strip())
    return sorted(counties)

# 取得指定縣市的所有區域
def getDistrictOptions(bookstoreList, cityName):
    districts = set()
    for store in bookstoreList:
        if store.get("cityName") and store.get("cityName").strip() == cityName:
            dist = store.get("townName")
            if dist:
                districts.add(dist.strip())
    return sorted(districts)

# 取得符合條件的書店
def getSpecificBookstore(bookstoreList, cityName, districtList):
    result = []
    for store in bookstoreList:
        if store.get("cityName", "").strip() == cityName and store.get("townName", "").strip() in districtList:
            result.append(store)
    return result

# 顯示書店資訊
def getBookstoreInfo(bookstoreList):
    for store in bookstoreList:
        with st.expander(store.get("name", "未知書店")):
            st.image(store.get("representImage", ""), use_column_width=True)
            st.metric("點閱率", store.get("hitRate", "N/A"))
            st.subheader("📖 簡介")
            st.write(store.get("introduction", "無簡介"))
            st.subheader("📍 地址")
            st.write(store.get("address", "無地址"))
            st.subheader("⏰ 營業時間")
            st.write(store.get("openTime", "無營業時間"))
            st.subheader("📧 Email")
            st.write(store.get("email", "無 Email"))

# 主程式介面
def app():
    st.set_page_config(page_title="台灣特色書店地圖", layout="wide")
    st.header("📚 台灣特色書店地圖")
    
    # 取得資料
    bookstoreList = getAllBookstore()
    st.metric("📊 書店總數", len(bookstoreList))

    # 縣市選單
    countyOptions = getCountyOptions(bookstoreList)
    selectedCounty = st.selectbox("請選擇縣市", countyOptions)

    # 區域選單
    districtOptions = getDistrictOptions(bookstoreList, selectedCounty)
    selectedDistricts = st.multiselect("請選擇行政區域（可複選）", districtOptions)

    # 篩選書店
    if selectedDistricts:
        filteredBookstore = getSpecificBookstore(bookstoreList, selectedCounty, selectedDistricts)
        st.success(f"找到 {len(filteredBookstore)} 間書店")
        
        # 選擇排序
        if st.checkbox("依據熱門程度排序（點閱率）"):
            filteredBookstore.sort(key=lambda x: x.get("hitRate", 0), reverse=True)
        
        getBookstoreInfo(filteredBookstore)
    else:
        st.info("請選擇行政區以顯示書店資訊。")

# 執行程式
if __name__ == "__main__":
    app()
