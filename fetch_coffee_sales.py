from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def generate_coffee_dataset():
  np.random.seed(123)
  n_rows = 1500

  # Tanggal transaksi dalam 60 hari terakhir
  end_date = datetime.now()
  start_date = end_date - timedelta(days=60)
  date_list = [
      start_date + timedelta(days=int(np.random.randint(0, 60)))
      for _ in range(n_rows)
  ]

  cities = [
      "Jakarta",
      "Bandung",
      "Surabaya",
      "Yogyakarta",
      "Bali",
      "Medan",
  ]
  city_weights = [0.30, 0.25, 0.20, 0.10, 0.10, 0.05]

  brands = [
      "Kopi Kenangan Style",
      "Fore Coffee Style",
      "Janji Jiwa Style",
      "Local Artisan Cafe",
  ]

  categories = [
      "Espresso Based",
      "Manual Brew",
      "Non-Coffee",
      "Pastry & Food",
  ]
  cat_weights = [0.45, 0.15, 0.25, 0.15]

  payments = ["QRIS", "E-Wallet (GoPay/OVO/DANA)", "Credit Card", "Cash"]
  pay_weights = [0.55, 0.25, 0.10, 0.10]

  data = []
  for i in range(n_rows):
    city = np.random.choice(cities, p=city_weights)
    brand = np.random.choice(brands)
    cat = np.random.choice(categories, p=cat_weights)
    pay = np.random.choice(payments, p=pay_weights)

    # Penentuan item dan harga (dalam Rupiah)
    if cat == "Espresso Based":
      item = np.random.choice(
          ["Caffè Latte", "Caramel Macchiato", "Americano", "Kopi Susu Gula Aren"]
      )
      price = int(np.random.randint(22000, 45000))
    elif cat == "Manual Brew":
      item = np.random.choice(
          ["V60 Gayo", "Tubruk Toraja", "Japanese Iced Coffee", "Vietnam Drip"]
      )
      price = int(np.random.randint(25000, 40000))
    elif cat == "Non-Coffee":
      item = np.random.choice(
          ["Matcha Latte", "Chocolate Regal", "Taro Latte", "Lychee Tea"]
      )
      price = int(np.random.randint(25000, 48000))
    else:  # Pastry & Food
      item = np.random.choice(
          ["Butter Croissant", "Smoked Beef Cheese Sandwich", "Cinnamon Roll"]
      )
      price = int(np.random.randint(30000, 65000))

    qty = int(np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1]))
    revenue = price * qty
    rating = round(
        float(np.random.choice([4.0, 4.5, 4.8, 5.0], p=[0.1, 0.2, 0.3, 0.4])), 1
    )

    data.append({
        "transaction_id": f"TRX-{2000 + i}",
        "transaction_date": date_list[i].strftime("%Y-%m-%d"),
        "city": city,
        "coffee_shop_brand": brand,
        "menu_category": cat,
        "item_name": item,
        "unit_price_idr": price,
        "quantity": qty,
        "total_revenue_idr": revenue,
        "payment_method": pay,
        "customer_rating": rating,
    })

  df = pd.DataFrame(data)
  filename = "indonesia_coffee_shop_sales.csv"
  df.to_csv(filename, index=False)
  print(
      f"Success! Dataset generated with {len(df)} records and saved as"
      f" '{filename}'"
  )


if __name__ == "__main__":
  generate_coffee_dataset()
