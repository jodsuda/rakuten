import streamlit as st
import requests
import urllib.parse
import pandas as pd

# ✅ 楽天APIキー & アフィリエイトID
API_KEY = "1049309157477690132"  # ← 自分のAPIキーに変更！
AFFILIATE_ID = "469658c6.99518438.469658c7.a3387bd1"  # ← 自分のアフィリエイトIDに変更！

# ✅ カテゴリ選択
category_options = {
    "（カテゴリを選択）": "",
    "韓国ファッション": "100371",
    "香水・コスメ": "100939",
    "インテリア雑貨": "101164",
    "スニーカー": "558885",
    "美容家電": "100227",
    "カフェ雑貨": "558944",
    "推し活グッズ": "101164"
}
st.title("🛒 楽天アフィリエイト検索ツール")
st.write("カテゴリ選択 or 自由検索で楽天市場の商品を探せます📦")

selected_category = st.selectbox("▼ カテゴリを選ぶ", list(category_options.keys()))
category_id = category_options[selected_category]

# ✅ 検索キーワード
keyword = st.text_input("🔍 キーワードを入力", value="")

# ✅ 検索ボタン
if st.button("商品を検索する"):
    if not keyword:
        st.warning("キーワードを入力してください。")
    else:
        # ✅ API URL組み立て
        base_url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
        params = {
            "applicationId": API_KEY,
            "keyword": keyword,
            "format": "json",
            "hits": 30
        }
        if category_id:
            params["genreId"] = category_id

        response = requests.get(base_url, params=params)
        data = response.json()
        items = data.get("Items", [])

        if not items:
            st.info("商品が見つかりませんでした。別のキーワードで試してください。")
        else:
            st.write("### 🛍 商品一覧")
            product_list = []

            for item in items:
                product = item["Item"]
                image_url = product["mediumImageUrls"][0]["imageUrl"]
                name = product["itemName"]
                price = f"{product['itemPrice']} 円"
                shop = product["shopName"]
                encoded_url = urllib.parse.quote(product["itemUrl"], safe='')
                affiliate_url = f"https://hb.afl.rakuten.co.jp/hgc/{AFFILIATE_ID}/?pc={encoded_url}&m={encoded_url}"

                # 表示用
                st.image(image_url, width=150)
                st.markdown(f"**[{name}]({affiliate_url})**")
                st.write(f"{price}｜{shop}")
                st.markdown("---")

                # CSV用
                product_list.append({
                    "商品名": name,
                    "価格": price,
                    "ショップ": shop,
                    "アフィリエイトリンク": affiliate_url
                })

            # CSVダウンロード
            df = pd.DataFrame(product_list)
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="💾 商品一覧をCSVで保存",
                data=csv,
                file_name="rakuten_items.csv",
                mime="text/csv"
            )
