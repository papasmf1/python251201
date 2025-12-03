import sqlite3
from typing import Optional, List, Tuple

class ProductsDB:
    def __init__(self, db_path: str = r"c:\work\MyProduct.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_table()

    def _ensure_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products (
            productID INTEGER PRIMARY KEY,
            productName TEXT NOT NULL,
            productPrice INTEGER NOT NULL
        );
        """
        self.conn.execute(sql)
        self.conn.commit()

    def insert_product(self, productID: int, productName: str, productPrice: int):
        sql = "INSERT OR REPLACE INTO Products (productID, productName, productPrice) VALUES (?, ?, ?)"
        self.conn.execute(sql, (productID, productName, productPrice))
        self.conn.commit()

    def bulk_insert_products(self, total: int = 100_000, batch_size: int = 5000):
        """
        빠른 대량 삽입: 배치 단위로 트랜잭션을 묶어 커밋합니다.
        productName은 "Product {id}", productPrice는 간단한 수식으로 생성됩니다.
        """
        insert_sql = "INSERT OR REPLACE INTO Products (productID, productName, productPrice) VALUES (?, ?, ?)"
        start_id = 1
        cur = self.conn.cursor()

        # 이미 일부 데이터가 있으면 이어서 삽입
        cur.execute("SELECT COUNT(1) FROM Products")
        existing = cur.fetchone()[0]
        if existing >= total:
            return

        start_id = existing + 1
        remaining = total - existing

        id_iter = range(start_id, start_id + remaining)
        batch = []
        for i in id_iter:
            name = f"Product {i}"
            price = (i % 1000) + 100  # 예: 100 ~ 1099
            batch.append((i, name, price))
            if len(batch) >= batch_size:
                cur.executemany(insert_sql, batch)
                self.conn.commit()
                batch.clear()
        if batch:
            cur.executemany(insert_sql, batch)
            self.conn.commit()

    def update_product(self, productID: int, productName: Optional[str] = None, productPrice: Optional[int] = None) -> bool:
        parts = []
        params: List = []
        if productName is not None:
            parts.append("productName = ?")
            params.append(productName)
        if productPrice is not None:
            parts.append("productPrice = ?")
            params.append(productPrice)
        if not parts:
            return False
        params.append(productID)
        sql = f"UPDATE Products SET {', '.join(parts)} WHERE productID = ?"
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur.rowcount > 0

    def delete_product(self, productID: int) -> bool:
        cur = self.conn.execute("DELETE FROM Products WHERE productID = ?", (productID,))
        self.conn.commit()
        return cur.rowcount > 0

    def select_product(self, productID: int) -> Optional[Tuple]:
        cur = self.conn.execute("SELECT productID, productName, productPrice FROM Products WHERE productID = ?", (productID,))
        row = cur.fetchone()
        if row:
            return (row["productID"], row["productName"], row["productPrice"])
        return None

    def select_all(self, limit: Optional[int] = None) -> List[Tuple]:
        sql = "SELECT productID, productName, productPrice FROM Products ORDER BY productID"
        if limit:
            sql += f" LIMIT {int(limit)}"
        cur = self.conn.execute(sql)
        return [(r["productID"], r["productName"], r["productPrice"]) for r in cur.fetchall()]

    def count(self) -> int:
        cur = self.conn.execute("SELECT COUNT(1) FROM Products")
        return cur.fetchone()[0]

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # 스크립트 실행 시 DB 생성 및 샘플 100,000개 준비
    db = ProductsDB(r"c:\work\MyProduct.db")
    print("현재 레코드 수:", db.count())
    TARGET = 100_000
    if db.count() < TARGET:
        print(f"{TARGET}개 샘플 데이터 생성 시작...")
        db.bulk_insert_products(total=TARGET, batch_size=5000)
        print("삽입 완료. 현재 레코드 수:", db.count())
    else:
        print("이미 충분한 데이터가 있습니다.")
    # 샘플 출력(앞 5개)
    sample = db.select_all(limit=5)
    for row in sample:
        print(row)
    db.close()